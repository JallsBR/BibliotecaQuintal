from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
import os

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

class Autor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nome']

class Editora(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'
        ordering = ['nome']

class Livro(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    descricao = models.TextField(blank=True, null=True)
    pontuacao = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Pontuação', blank=True, null=True)
    qtd_paginas = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Quantidade de Páginas', blank=True, null=True)
    ano_publicacao = models.IntegerField(
        validators=[MinValueValidator(1900)],
        verbose_name='Ano de Publicação',
        blank=True,
        null=True,
    )
    qtd_total = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Quantidade total',
        default=1,
        help_text='Total de exemplares do livro na biblioteca.',
    )
    qtd_emprestados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Quantidade Emprestados', default=0)
    is_disponivel = models.BooleanField(default=True, verbose_name='Disponível', blank=True, null=True)
    idioma = models.CharField(max_length=50, verbose_name='Idioma', blank=True, null=True)
    isbn = models.CharField(max_length=13, verbose_name='ISBN', blank=True, null=True)
    ativo = models.BooleanField(default=True, verbose_name='Ativo', blank=True, null=True)
    imagem = models.ImageField(upload_to='livros/', blank=True, null=True, verbose_name='Imagem')
    imagem_url = models.URLField(blank=True, null=True, verbose_name='URL da Imagem')
    autores = models.ManyToManyField(Autor, verbose_name='Autores', blank=True)
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE, verbose_name='Editora', blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, verbose_name='Categorias', blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        autores_nomes = ", ".join(self.autores.values_list("nome", flat=True)) if self.pk else ""
        categorias_nomes = ", ".join(self.categorias.values_list("nome", flat=True)) if self.pk else ""
        return f"{self.titulo} - {autores_nomes} - {self.editora} - {categorias_nomes}"

    @property
    def qtd_disponivel(self):
        """Quantidade disponível = quantidade total - quantidade emprestados. Calculado dinamicamente."""
        total = self.qtd_total if self.qtd_total is not None else 0
        emp = self.qtd_emprestados if self.qtd_emprestados is not None else 0
        return max(0, total - emp)

    def clean(self):
        qtd_total = self.qtd_total if self.qtd_total is not None else 0
        qtd_pag = self.qtd_paginas
        ano = self.ano_publicacao
        if self.qtd_total is not None and self.qtd_total < 0:
            raise ValidationError("A quantidade total não pode ser menor que 0.")
        if (self.qtd_emprestados or 0) < 0:
            raise ValidationError("A quantidade de livros emprestados não pode ser menor que 0.")
        disp = self.qtd_disponivel
        if qtd_total > 0 and disp > qtd_total:
            raise ValidationError("A quantidade disponível não pode ser maior que a quantidade total.")
        if ano is not None and ano > timezone.now().year:
            raise ValidationError("O ano de publicação não pode ser maior que o ano atual.")
        if qtd_pag is not None and qtd_pag < 1:
            raise ValidationError("A quantidade de páginas não pode ser menor que 1.")
        if ano is not None and ano < 1900:
            raise ValidationError("O ano de publicação não pode ser menor que 1900.")
    
    def save(self, *args, **kwargs):
        if self.qtd_total is not None and self.qtd_emprestados is not None:
            self.is_disponivel = (self.qtd_total - self.qtd_emprestados) > 0

        # Primeiro salva normalmente
        super().save(*args, **kwargs)

        # Otimiza a imagem se existir
        if self.imagem:
            try:
                img_path = self.imagem.path
                img = Image.open(img_path)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                width, height = img.size
                min_dim = min(width, height)
                left = (width - min_dim) / 2
                top = (height - min_dim) / 2
                right = (width + min_dim) / 2
                bottom = (height + min_dim) / 2
                img = img.crop((left, top, right, bottom))

                img = img.resize((400, 400), Image.Resampling.LANCZOS)

                buffer = BytesIO()
                img.save(buffer, format="JPEG", quality=85, optimize=True)
                buffer.seek(0)

                file_name = os.path.basename(img_path)
                self.imagem.save(file_name, ContentFile(buffer.read()), save=False)

                super().save(update_fields=["imagem"])
            except Exception as e:
                print(f"[ERRO] Falha ao otimizar imagem: {e}")
    
 
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['titulo']
