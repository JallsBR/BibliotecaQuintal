# Generated manually for LeitorRecompensa (through model with data_resgate)

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


def migrate_recompensas_to_through(apps, schema_editor):
    """Copia dados da tabela antiga do M2M para LeitorRecompensa com data_resgate=hoje."""
    LeitorRecompensa = apps.get_model('leitor', 'LeitorRecompensa')
    today = django.utils.timezone.localdate()
    conn = schema_editor.connection
    with conn.cursor() as cursor:
        # Tabela antiga do M2M implícito (Django default: app_model_field)
        cursor.execute(
            "SELECT leitor_id, recompensa_id FROM leitor_leitor_recompensas"
        )
        rows = cursor.fetchall()
    for leitor_id, recompensa_id in rows:
        LeitorRecompensa.objects.using(schema_editor.connection.alias).create(
            leitor_id=leitor_id,
            recompensa_id=recompensa_id,
            data_resgate=today
        )


def reverse_migrate(apps, schema_editor):
    """Não há reversão segura (dados de data_resgate seriam perdidos)."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('leitor', '0011_alter_reserva_data_expiracao'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeitorRecompensa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_resgate', models.DateField(default=django.utils.timezone.now, verbose_name='Data do resgate')),
                ('leitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leitor.leitor')),
                ('recompensa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leitor.recompensa')),
            ],
            options={
                'verbose_name': 'Resgate de recompensa',
                'verbose_name_plural': 'Resgates de recompensa',
                'ordering': ['-data_resgate', 'recompensa__nome'],
                'unique_together': {('leitor', 'recompensa')},
            },
        ),
        migrations.RunPython(migrate_recompensas_to_through, reverse_migrate),
        migrations.RemoveField(
            model_name='leitor',
            name='recompensas',
        ),
        migrations.AddField(
            model_name='leitor',
            name='recompensas',
            field=models.ManyToManyField(
                blank=True,
                related_name='leitores_resgataram',
                through='leitor.LeitorRecompensa',
                to='leitor.recompensa',
            ),
        ),
    ]
