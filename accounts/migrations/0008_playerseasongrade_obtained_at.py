# Generated by Django 4.0.4 on 2022-05-23 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_rename_rank_level_rank_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerseasongrade',
            name='obtained_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
