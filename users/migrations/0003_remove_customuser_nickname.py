# Generated by Django 5.2.1 on 2025-05-30 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='nickname',
        ),
    ]
