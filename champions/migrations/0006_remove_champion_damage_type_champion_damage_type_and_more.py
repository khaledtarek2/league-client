# Generated by Django 4.0.4 on 2022-05-23 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('champions', '0005_alter_champion_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champion',
            name='damage_Type',
        ),
        migrations.AddField(
            model_name='champion',
            name='damage_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Attack Damage'), (1, 'Ability Power')], null=True),
        ),
        migrations.AlterField(
            model_name='champion',
            name='category',
            field=models.IntegerField(blank=True, choices=[(0, 'Damage'), (1, 'Toughness'), (2, 'Crowd Control'), (3, 'Mobility'), (4, 'Utility')], null=True),
        ),
        migrations.AlterField(
            model_name='champion',
            name='description',
            field=models.TextField(),
        ),
    ]
