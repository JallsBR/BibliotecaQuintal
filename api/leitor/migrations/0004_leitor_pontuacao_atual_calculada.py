# Pontuacao_atual passa a ser propriedade calculada (total - recompensas)
# Pontuacao_total ganha MinValueValidator(0)

from django.db import migrations, models
from django.core.validators import MinValueValidator


class Migration(migrations.Migration):

    dependencies = [
        ('leitor', '0003_add_pontuacao_creditada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leitor',
            name='pontuacao_atual',
        ),
        migrations.AlterField(
            model_name='leitor',
            name='pontuacao_total',
            field=models.IntegerField(
                default=0,
                validators=[MinValueValidator(0)],
                verbose_name='Pontuação total acumulada',
            ),
        ),
    ]
