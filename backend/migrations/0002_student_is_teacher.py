# Generated by Django 5.2 on 2025-04-19 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
