# Generated by Django 4.1.7 on 2023-06-26 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import patolsima_api.apps.uploaded_file_management.models
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('uploaded_file_management', '0004_uploadedfile_extra'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalUploadedFile',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('uuid', models.CharField(db_index=True, default=patolsima_api.apps.uploaded_file_management.models.get_uuid_for_new_file, max_length=36)),
                ('file_name', models.CharField(max_length=512)),
                ('local_filepath', models.CharField(blank=True, max_length=512, null=True)),
                ('storage_unit', models.CharField(choices=[('AWS_S3', 'Aws S3'), ('LOCAL_STORAGE', 'Local Storage')], default='LOCAL_STORAGE', max_length=16)),
                ('size', models.IntegerField()),
                ('content_type', models.CharField(blank=True, max_length=64, null=True)),
                ('object_key', models.CharField(blank=True, max_length=512, null=True)),
                ('bucket_name', models.CharField(blank=True, max_length=256, null=True)),
                ('extra', models.JSONField(blank=True, null=True)),
                ('last_time_requested', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical uploaded file',
                'verbose_name_plural': 'historical uploaded files',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]