# Generated by Django 5.0.6 on 2024-08-13 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_remove_post_tasks_post_search__3e7775_gin_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='post',
            name='title_trgm_idx',
        ),
        migrations.RemoveIndex(
            model_name='post',
            name='body_trgm_idx',
        ),
    ]
