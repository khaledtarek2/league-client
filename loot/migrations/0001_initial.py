# Generated by Django 4.0.4 on 2022-05-23 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('loot_type', models.IntegerField(choices=[(0, 'Ward Skin'), (1, 'Skin'), (2, 'Champion'), (3, 'Material'), (4, 'Tactical'), (5, 'Eternal'), (6, 'Emote'), (7, 'Icon')])),
                ('loot_currency', models.IntegerField(choices=[(0, 'Blue Essence'), (1, 'Orange Essence'), (2, 'Event Coins')])),
            ],
        ),
        migrations.CreateModel(
            name='LootOwnerShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid', models.IntegerField()),
                ('purchasing_currency', models.IntegerField(choices=[(0, 'Blue Essence'), (1, 'Orange Essence'), (2, 'Event Coins')])),
                ('loot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loot.loot')),
            ],
        ),
    ]
