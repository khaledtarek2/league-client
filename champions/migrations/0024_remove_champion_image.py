# Generated by Django 4.0.4 on 2022-06-06 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0023_alter_championmastery_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champion',
            name='image',
        ),
    ]
