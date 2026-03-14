from datetime import timedelta

from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from users.models import User
from users.validators import validate_cpf, validate_telefone
from django.utils import timezone
from livros.models import Livro


# Create your models here.
class Recompensa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    pontuacao = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Recompensa'
        verbose_name_plural = 'Recompensas'
        ordering = ['pontuacao', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.descricao} - {self.pontuacao}"



class Leitor(models.Model):
    nome = models.CharField(max_length=250)
    livros_lidos = models.ManyToManyField(Livro, blank=True)
    recompensas = models.ManyToManyField(Recompensa, blank=True)
    pontuacao_total = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Pontuação total acumulada',
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True) 
    sexo = models.CharField(max_length=10, blank=True, null=True, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')])
    profissao = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True, validators=[validate_telefone])
    endereco = models.CharField(max_length=250, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True, validators=[validate_cpf])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Leitor'
        verbose_name_plural = 'Leitores'
        ordering = ['nome']

    @property
    def pontuacao_atual(self):
        """
        Pontuação disponível = pontuacao_total - soma das pontuações das recompensas
        que o leitor já recebeu. Nunca menor que zero.
        """
        total = self.pontuacao_total or 0
        if not self.pk:
            return max(0, total)
        gasto = self.recompensas.aggregate(s=Sum('pontuacao'))['s'] or 0
        return max(0, total - gasto)

    def clean(self):
        if self.pontuacao_total is not None and self.pontuacao_total < 0:
            raise ValidationError({'pontuacao_total': 'A pontuação total não pode ser negativa.'})

    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(default=timezone.localdate)
    data_devolucao = models.DateField(
        null=True,
        blank=True,
        help_text='Previsão de devolução; a devolução efetiva ocorre quando devolvido=True.'
    )
    devolvido = models.BooleanField(default=False)
    pontuacao_creditada = models.BooleanField(
        default=False,
        verbose_name='Pontuação já creditada ao leitor',
        help_text='Marcado quando a pontuação do livro foi somada ao pontuacao_total do leitor.'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'
        ordering = ['data_emprestimo']

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.data_devolucao:
                self.data_devolucao = self.data_emprestimo + timedelta(days=15)
        super().save(*args, **kwargs)

    def clean(self):
        # Validações de livro só ao EMPRESTAR (novo registro). Devolução (devolvido=True) sempre permitida.
        if not self.pk and self.livro_id:
            if not self.livro.ativo:
                raise ValidationError(
                    {"livro": "Livro inativo. Não pode ser emprestado."}
                )
            qtd_disponivel = self.livro.qtd_disponivel or 0
            if qtd_disponivel < 1:
                raise ValidationError(
                    {"livro": "Não há exemplares disponíveis para empréstimo."}
                )
            reservas_ativas = Reserva.objects.filter(
                livro_id=self.livro_id,
                ativo=True,
                data_expiracao__gte=timezone.localdate(),
            ).count()
            # Bloqueia se há reservas que já "ocupam" os exemplares disponíveis (prioridade para quem reservou)
            if reservas_ativas >= qtd_disponivel:
                raise ValidationError(
                    {"livro": "Livro em reserva. Priorize a entrega para quem reservou."}
                )
        if self.data_devolucao and self.data_devolucao < self.data_emprestimo:
            raise ValidationError("A data de devolução (previsão) não pode ser anterior à data de empréstimo.")
        # Só exige data_emprestimo >= hoje na criação; na atualização (ex.: marcar devolvido) permite datas passadas
        if not self.pk and self.data_emprestimo and self.data_emprestimo < timezone.localdate():
            raise ValidationError("A data de empréstimo não pode ser menor que a data atual.")
        if self.data_devolucao and self.data_emprestimo > self.data_devolucao:
            raise ValidationError("A data de empréstimo não pode ser maior que a data de devolução (previsão).")


    def __str__(self):
        return f"{self.leitor} - {self.livro} - {self.data_emprestimo}"


class Reserva(models.Model):
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_reserva = models.DateField(default=timezone.localdate)
    data_expiracao = models.DateField(
        null=True,
        blank=True,
        help_text='Se não informada, será preenchida automaticamente com data_reserva + 15 dias.'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['data_reserva']

    def save(self, *args, **kwargs):
        if not self.pk and self.data_reserva and not self.data_expiracao:
            self.data_expiracao = self.data_reserva + timedelta(days=15)
        super().save(*args, **kwargs)

    def clean(self):
        # Só exige datas >= hoje na criação; na atualização (ex.: cancelar) permite datas passadas
        if not self.pk:
            if self.data_expiracao and self.data_expiracao < timezone.localdate():
                raise ValidationError("A data de expiração não pode ser menor que a data atual.")
            if self.data_reserva and self.data_reserva < timezone.localdate():
                raise ValidationError("A data de reserva não pode ser menor que a data atual.")
        if self.data_reserva and self.data_expiracao and self.data_reserva > self.data_expiracao:
            raise ValidationError("A data de reserva não pode ser maior que a data de expiração.")

    def __str__(self):
        return f"{self.leitor} - {self.livro} - {self.data_reserva}"




