# Generated by Django 4.2.16 on 2024-10-14 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqlscope', '0010_server_fk_engine_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
