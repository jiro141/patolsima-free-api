# Generated by Django 4.1.7 on 2023-10-31 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_historicalmedicotratante_ci_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalinforme',
            name='muestra_recibida',
            field=models.TextField(blank=True, max_length=10240, null=True),
        ),
        migrations.AddField(
            model_name='informe',
            name='muestra_recibida',
            field=models.TextField(blank=True, max_length=10240, null=True),
        ),
    ]
