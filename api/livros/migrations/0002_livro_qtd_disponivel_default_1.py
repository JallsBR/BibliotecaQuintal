# Ao cadastrar livro, qtd_disponivel deve ser 1 (não nulo, default=1)

from django.db import migrations, models
from django.core.validators import MinValueValidator


def preencher_qtd_disponivel_nulos(apps, schema_editor):
    Livro = apps.get_model('livros', 'Livro')
    Livro.objects.filter(qtd_disponivel__isnull=True).update(qtd_disponivel=1)


def reverter(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(preencher_qtd_disponivel_nulos, reverter),
        migrations.AlterField(
            model_name='livro',
            name='qtd_disponivel',
            field=models.IntegerField(
                blank=True,
                default=1,
                validators=[MinValueValidator(0)],
                verbose_name='Quantidade Disponível',
            ),
        ),
    ]
