# Generated by Django 4.0.4 on 2022-06-02 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_remove_profile_highest_champion_mastery'),
        ('champions', '0017_alter_championmastery_champion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championmastery',
            name='champion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mastries', to='champions.champion'),
        ),
        migrations.AlterField(
            model_name='championmastery',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mastries', to='accounts.profile'),
        ),
    ]
