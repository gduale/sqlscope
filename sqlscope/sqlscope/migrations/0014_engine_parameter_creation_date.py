# Generated by Django 4.2.16 on 2024-12-27 18:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sqlscope', '0013_engine_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='engine_parameter',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
