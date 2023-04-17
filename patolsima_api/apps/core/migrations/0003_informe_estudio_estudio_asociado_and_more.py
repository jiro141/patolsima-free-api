# Generated by Django 4.1.7 on 2023-04-17 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('s3_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_alter_paciente_ci'),
    ]

    operations = [
        migrations.CreateModel(
            name='Informe',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('estudio', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core.estudio')),
                ('descripcion_macroscopica', models.TextField(blank=True, max_length=10240, null=True)),
                ('descripcion_microscopica', models.TextField(blank=True, max_length=10240, null=True)),
                ('diagnostico', models.TextField(blank=True, max_length=10240, null=True)),
                ('notas', models.TextField(blank=True, max_length=10240, null=True)),
                ('anexos', models.TextField(blank=True, max_length=10240, null=True)),
                ('bibliografia', models.TextField(blank=True, max_length=10240, null=True)),
                ('completado', models.BooleanField(default=False)),
                ('aprobado', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='estudio',
            name='estudio_asociado',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='historicalestudio',
            name='estudio_asociado',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.CreateModel(
            name='ResultadoInmunostoquimica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('procedimiento', models.CharField(max_length=256)),
                ('reaccion', models.CharField(max_length=256)),
                ('diagnostico_observaciones', models.TextField(blank=True, max_length=1024, null=True)),
                ('informe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultadod_inmunostoquimica', to='core.informe')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InformeGenerado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('informe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.informe')),
                ('s3_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='s3_management.s3file')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='informe',
            name='informes_generados',
            field=models.ManyToManyField(through='core.InformeGenerado', to='s3_management.s3file'),
        ),
        migrations.CreateModel(
            name='HistoricalResultadoInmunostoquimica',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('procedimiento', models.CharField(max_length=256)),
                ('reaccion', models.CharField(max_length=256)),
                ('diagnostico_observaciones', models.TextField(blank=True, max_length=1024, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('informe', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.informe')),
            ],
            options={
                'verbose_name': 'historical resultado inmunostoquimica',
                'verbose_name_plural': 'historical resultado inmunostoquimicas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInforme',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('descripcion_macroscopica', models.TextField(blank=True, max_length=10240, null=True)),
                ('descripcion_microscopica', models.TextField(blank=True, max_length=10240, null=True)),
                ('diagnostico', models.TextField(blank=True, max_length=10240, null=True)),
                ('notas', models.TextField(blank=True, max_length=10240, null=True)),
                ('anexos', models.TextField(blank=True, max_length=10240, null=True)),
                ('bibliografia', models.TextField(blank=True, max_length=10240, null=True)),
                ('completado', models.BooleanField(default=False)),
                ('aprobado', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('estudio', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.estudio')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical informe',
                'verbose_name_plural': 'historical informes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
