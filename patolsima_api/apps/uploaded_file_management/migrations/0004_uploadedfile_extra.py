# Generated by Django 4.1.7 on 2023-06-26 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploaded_file_management', '0003_uploadedfile_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='extra',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
