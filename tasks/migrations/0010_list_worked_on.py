# Generated by Django 5.0.6 on 2024-08-21 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_post_options_post_deadline_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='worked_on',
            field=models.IntegerField(choices=[(0, 'Office'), (1, 'Manufacturer'), (2, 'Customer'), (3, 'Home')], default=0),
        ),
    ]
