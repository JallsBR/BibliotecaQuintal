# Generated for signal: creditar pontuação ao leitor quando empréstimo tem data_devolucao

from django.db import migrations, models


def marcar_existentes_como_creditados(apps, schema_editor):
    """Empréstimos já existentes não devem receber crédito de pontuação novamente."""
    Emprestimo = apps.get_model('leitor', 'Emprestimo')
    Emprestimo.objects.all().update(pontuacao_creditada=True)


def reverter(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('leitor', '0002_leitor_sexo_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='emprestimo',
            name='pontuacao_creditada',
            field=models.BooleanField(
                default=False,
                help_text='Marcado quando a pontuação do livro foi somada ao pontuacao_total do leitor.',
                verbose_name='Pontuação já creditada ao leitor'
            ),
        ),
        migrations.RunPython(marcar_existentes_como_creditados, reverter),
    ]
