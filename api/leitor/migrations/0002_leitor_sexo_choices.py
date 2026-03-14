# Generated manually for choices on sexo

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leitor',
            name='sexo',
            field=models.CharField(
                blank=True,
                choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
                max_length=10,
                null=True
            ),
        ),
    ]
