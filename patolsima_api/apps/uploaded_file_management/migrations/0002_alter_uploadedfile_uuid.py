# Generated by Django 4.1.7 on 2023-05-08 00:32

from django.db import migrations, models
import patolsima_api.apps.uploaded_file_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('uploaded_file_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='uuid',
            field=models.CharField(db_index=True, default=patolsima_api.apps.uploaded_file_management.models.get_uuid_for_new_file, max_length=36, unique=True),
        ),
    ]
