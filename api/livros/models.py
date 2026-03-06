from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nome']

class Editora(models.Model):
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'
        ordering = ['nome']

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    pontuacao = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Pontuação', blank=True, null=True)
    qtd_paginas = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Quantidade de Páginas', blank=True, null=True)
    ano_publicacao = models.IntegerField(validators=[MinValueValidator(1900)], verbose_name='Ano de Publicação', blank=True, null=True  )
    qtd_disponivel = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Quantidade Disponível', blank=True, null=True)
    qtd_emprestados = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Quantidade Emprestados', blank=True, null=True)
    is_disponivel = models.BooleanField(default=True, verbose_name='Disponível', blank=True, null=True)
    idioma = models.CharField(max_length=50, verbose_name='Idioma', blank=True, null=True)
    isbn = models.CharField(max_length=13, verbose_name='ISBN', blank=True, null=True)
    ativo = models.BooleanField(default=True, verbose_name='Ativo', blank=True, null=True)
    imagem = models.ImageField(upload_to='livros/', blank=True, null=True, verbose_name='Imagem')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, verbose_name='Autor', blank=True, null=True)
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE, verbose_name='Editora', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return self.titulo  -{self.autor} -{self.editora} -{self.categoria}

    def clean(self):
        if self.qtd_disponivel > self.qtd_paginas:
            raise ValidationError("A quantidade de livros disponíveis não pode ser maior que a quantidade de páginas.")
        if self.ano_publicacao > timezone.now().year:
            raise ValidationError("O ano de publicação não pode ser maior que o ano atual.")
        if self.qtd_paginas < 1:
            raise ValidationError("A quantidade de páginas não pode ser menor que 1.")
        if self.ano_publicacao < 1900:
            raise ValidationError("O ano de publicação não pode ser menor que 1900.")
        if self.qtd_disponivel < 0:
            raise ValidationError("A quantidade de livros disponíveis não pode ser menor que 0.")
    
    def save(self, *args, **kwargs):
        # is_disponivel: False se qtd_disponivel == qtd_emprestados, True caso contrário
        if self.qtd_disponivel is not None and self.qtd_emprestados is not None:
            self.is_disponivel = (self.qtd_disponivel != self.qtd_emprestados)
        try:
            super().save(*args, **kwargs)

            if self.photo:
                img_path = self.photo.path
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
                img.save(buffer, format='JPEG', quality=85, optimize=True)
                buffer.seek(0)

                file_name = os.path.basename(img_path)
                self.photo.save(file_name, ContentFile(buffer.read()), save=False)

                super().save(update_fields=['photo'])
        except Exception as e:
            print(f"[ERRO] Falha ao otimizar imagem: {e}")
    
 
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'
        ordering = ['titulo','autor','editora','categoria']
