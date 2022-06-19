# Generated by Django 4.0.4 on 2022-05-23 02:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loot', '0002_lootownership_player'),
        ('champions', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='championownership',
            name='champion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='champions.champion'),
        ),
        migrations.AddField(
            model_name='championownership',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='champions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='player',
            name='owned_champions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='champions.champion'),
        ),
        migrations.AddField(
            model_name='player',
            name='owned_loot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loot.loot'),
        ),
        migrations.AddField(
            model_name='player',
            name='owned_skins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='champions.championskin'),
        ),
        migrations.AddField(
            model_name='playerseasongrade',
            name='champion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='season_grades', to='champions.champion'),
        ),
        migrations.AddField(
            model_name='playerseasongrade',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='season_grades', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='highest_champion_mastery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='champions.championmastery'),
        ),
        migrations.AddField(
            model_name='skinownership',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skins', to=settings.AUTH_USER_MODEL),
        ),
    ]
