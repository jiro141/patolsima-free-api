# Generated by Django 4.1.7 on 2023-03-30 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_estudio_prioridad_estudio_tipo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estudio',
            name='prioridad',
        ),
        migrations.RemoveField(
            model_name='historicalestudio',
            name='prioridad',
        ),
        migrations.AddField(
            model_name='estudio',
            name='envio_digital',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='estudio',
            name='urgente',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalestudio',
            name='envio_digital',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='historicalestudio',
            name='urgente',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='muestra',
            name='estudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='muestras', to='core.estudio'),
        ),
    ]
