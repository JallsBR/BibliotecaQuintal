from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
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
    pontuacao_atual = models.IntegerField(default=0)
    pontuacao_total = models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10, blank=True, null=True)
    profissao = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=250, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Leitor'
        verbose_name_plural = 'Leitores'
        ordering = ['nome']    

    def __str__(self):
        return self.nome

class Emprestimo(models.Model):
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(default=timezone.now)
    data_devolucao = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'
        ordering = ['data_emprestimo']

    def clean(self):
        if self.livro and not self.livro.is_disponivel:
            raise ValidationError(
                {"livro": "Cadastre primeiro a devolução anterior."}
            )
        if self.data_devolucao < timezone.now():
            raise ValidationError("A data de devolução não pode ser menor que a data atual.")
        if self.data_emprestimo < timezone.now():
            raise ValidationError("A data de empréstimo não pode ser menor que a data atual.")
        if self.data_emprestimo > self.data_devolucao:
            raise ValidationError("A data de empréstimo não pode ser maior que a data de devolução.")


    def __str__(self):
        return f"{self.leitor} - {self.livro} - {self.data_emprestimo}"


class Reserva(models.Model):
    leitor = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(default=timezone.now)
    data_expiracao = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['data_reserva']

    def clean(self):
        if self.data_expiracao < timezone.now():
            raise ValidationError("A data de expiração não pode ser menor que a data atual.")
        if self.data_reserva < timezone.now():
            raise ValidationError("A data de reserva não pode ser menor que a data atual.")
        if self.data_reserva > self.data_expiracao:
            raise ValidationError("A data de reserva não pode ser maior que a data de expiração.")

    def __str__(self):
        return f"{self.leitor} - {self.livro} - {self.data_reserva}"




