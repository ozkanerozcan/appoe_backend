# Generated by Django 5.0.6 on 2024-08-13 07:24

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_post_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_at',)},
        ),
        TrigramExtension()
    ]
