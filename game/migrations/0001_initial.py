# Generated by Django 2.0 on 2018-03-12 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('value', models.PositiveSmallIntegerField(default=0)),
                ('worth', models.PositiveSmallIntegerField(default=0)),
                ('image_url', models.CharField(default='', max_length=100)),
                ('trump_priority', models.PositiveSmallIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trump', models.PositiveSmallIntegerField(choices=[(1, 'clubs'), (2, 'spades'), (3, 'hearts'), (4, 'diamonds')], default=1)),
                ('next_move', models.PositiveSmallIntegerField(choices=[(1, 'FIRST_PLAYER_NAME'), (2, 'SECOND_PLAYER_NAME'), (3, 'THIRD_PLAYER_NAME'), (4, 'FOURTH_PLAYER_NAME')], default=1)),
                ('total_moves', models.PositiveSmallIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='GameSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_save', models.IntegerField(choices=[(30, 'on_save_30'), (31, 'on_save_31')], default=30)),
                ('on_full', models.IntegerField(choices=[(1, 'on_full_open_four'), (2, 'on_full_finish_game')], default=1)),
                ('ace_allowed', models.BooleanField(default=True)),
                ('on_eggs', models.IntegerField(choices=[(1, 'on_eggs_open_four'), (2, 'on_eggs_open_double')], default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='game_setting', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Hand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('deck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hands', to='game.Deck')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user01_ready', models.BooleanField(default=False)),
                ('user02_ready', models.BooleanField(default=False)),
                ('user03_ready', models.BooleanField(default=False)),
                ('user04_ready', models.BooleanField(default=False)),
                ('all_ready', models.BooleanField(default=False)),
                ('full', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL)),
                ('user01', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user01', to=settings.AUTH_USER_MODEL)),
                ('user02', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user02', to=settings.AUTH_USER_MODEL)),
                ('user03', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user03', to=settings.AUTH_USER_MODEL)),
                ('user04', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user04', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.AddField(
            model_name='deck',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='decks', to='game.Room'),
        ),
        migrations.AddField(
            model_name='card',
            name='hand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='game.Hand'),
        ),
    ]
