# Generated by Django 4.1.7 on 2023-06-01 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_resultadoinmunostoquimica_informe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmedicotratante',
            name='ci',
            field=models.PositiveIntegerField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicotratante',
            name='ci',
            field=models.PositiveIntegerField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicotratante',
            name='ncomed',
            field=models.CharField(blank=True, db_index=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='ci',
            field=models.PositiveIntegerField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='patologo',
            name='ncomed',
            field=models.CharField(blank=True, db_index=True, max_length=32, null=True),
        ),
        migrations.AddConstraint(
            model_name='medicotratante',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted_at', None)), fields=('ncomed',), name='ncomed_unique_when_not_deleted'),
        ),
        migrations.AddConstraint(
            model_name='medicotratante',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted_at', None)), fields=('ci',), name='unique_constraint_only_for_not_deleted_ci_medico_tratante'),
        ),
        migrations.AddConstraint(
            model_name='paciente',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted_at', None)), fields=('ci',), name='unique_constraint_only_for_not_deleted_ci_paciente'),
        ),
        migrations.AddConstraint(
            model_name='patologo',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted_at', None)), fields=('ncomed',), name='patologo_ncomed_unique_when_not_deleted'),
        ),
    ]