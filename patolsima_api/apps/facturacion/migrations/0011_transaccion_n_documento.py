# Generated by Django 4.1.7 on 2023-11-24 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0010_remove_facturaoffset_factura_offset_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='n_documento',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
