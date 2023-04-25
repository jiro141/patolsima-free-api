# Generated by Django 4.1.7 on 2023-04-20 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_patologo_ncomed'),
        ('facturacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='ci_rif',
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='historicalcliente',
            name='ci_rif',
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='itemorden',
            name='estudio',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='items_orden', to='core.estudio'),
        ),
        migrations.AlterField(
            model_name='itemorden',
            name='orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_orden', to='facturacion.orden'),
        ),
        migrations.AlterField(
            model_name='notapago',
            name='pago',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nota_de_pago', to='facturacion.pago'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='facturacion.orden'),
        ),
    ]