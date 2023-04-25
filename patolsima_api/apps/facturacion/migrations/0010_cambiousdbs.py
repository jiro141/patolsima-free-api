# Generated by Django 4.1.7 on 2023-04-24 22:08

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0009_alter_factura_s3_file_alter_recibo_s3_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='CambioUSDBS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bs_e', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]