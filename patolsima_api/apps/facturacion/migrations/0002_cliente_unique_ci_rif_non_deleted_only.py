# Generated by Django 4.1.7 on 2023-06-01 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='cliente',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted_at', None)), fields=('ci_rif',), name='unique_ci_rif_non_deleted_only'),
        ),
    ]