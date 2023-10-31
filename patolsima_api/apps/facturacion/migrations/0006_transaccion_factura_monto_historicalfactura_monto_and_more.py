# Generated by Django 4.1.7 on 2023-10-31 16:10

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uploaded_file_management', '0005_historicaluploadedfile'),
        ('facturacion', '0005_facturaoffset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('archived', models.BooleanField(default=False)),
                ('rifci', models.CharField(max_length=50)),
                ('cliente', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=32)),
                ('n_control', models.PositiveIntegerField(db_index=True, unique=True)),
                ('monto', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('monto_impuesto', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('fecha_emision', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='factura',
            name='monto',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14),
        ),
        migrations.AddField(
            model_name='historicalfactura',
            name='monto',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14),
        ),
        migrations.CreateModel(
            name='NotaDebito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fecha_generacion', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('n_notadebito', models.PositiveIntegerField(db_index=True, unique=True)),
                ('monto', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('factura', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='facturacion.factura')),
                ('orden', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='facturacion.orden')),
                ('pago', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nota_de_debitos', to='facturacion.pago')),
                ('s3_file', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='uploaded_file_management.uploadedfile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NotaCredito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fecha_generacion', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('n_notacredito', models.PositiveIntegerField(db_index=True, unique=True)),
                ('monto', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=14)),
                ('factura', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='facturacion.factura')),
                ('orden', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='facturacion.orden')),
                ('pago', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nota_de_credito', to='facturacion.pago')),
                ('s3_file', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='uploaded_file_management.uploadedfile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]