# Generated by Django 4.2.16 on 2024-10-06 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqlscope', '0006_alter_server_status_engine_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='server_status',
            name='replication_status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
