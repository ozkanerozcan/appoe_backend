# Generated by Django 5.0.6 on 2024-08-13 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveIndex(
            model_name='customuser',
            name='first_name_trgm_idx',
        ),
    ]
