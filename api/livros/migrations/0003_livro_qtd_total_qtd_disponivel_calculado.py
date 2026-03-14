# qtd_total = total de exemplares; qtd_disponivel vira propriedade (total - emprestados)

from django.db import migrations, models
from django.core.validators import MinValueValidator


def preencher_qtd_total(apps, schema_editor):
    Livro = apps.get_model('livros', 'Livro')
    for livro in Livro.objects.all():
        disp = livro.qtd_disponivel if livro.qtd_disponivel is not None else 0
        emp = livro.qtd_emprestados if livro.qtd_emprestados is not None else 0
        livro.qtd_total = max(1, disp + emp)
        livro.save(update_fields=['qtd_total'])


def reverter(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0002_livro_qtd_disponivel_default_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='qtd_total',
            field=models.IntegerField(
                default=1,
                help_text='Total de exemplares do livro na biblioteca.',
                validators=[MinValueValidator(0)],
                verbose_name='Quantidade total',
            ),
            preserve_default=False,
        ),
        migrations.RunPython(preencher_qtd_total, reverter),
        migrations.RemoveField(
            model_name='livro',
            name='qtd_disponivel',
        ),
    ]
