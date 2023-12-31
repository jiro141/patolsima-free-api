# Generated by Django 4.1.7 on 2023-11-30 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0011_transaccion_n_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='orden',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='facturacion.orden'),
        ),
        migrations.AlterField(
            model_name='notascredito',
            name='orden',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='facturacion.orden'),
        ),
        migrations.AlterField(
            model_name='notasdebito',
            name='orden',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='facturacion.orden'),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='orden',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='facturacion.orden'),
        ),
    ]
