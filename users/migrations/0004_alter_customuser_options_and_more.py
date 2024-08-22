# Generated by Django 5.0.6 on 2024-08-13 12:33

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0003_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=django.contrib.postgres.indexes.GinIndex(fields=['first_name'], name='first_name_trgm_idx', opclasses=['gin_trgm_ops']),
        ),
    ]
