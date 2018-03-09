# Generated by Django 2.0 on 2018-03-09 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trump', models.PositiveSmallIntegerField(choices=[(1, 'clubs'), (2, 'spades'), (3, 'hearts'), (4, 'diamonds')], default=(1, 'clubs'))),
                ('next_move', models.PositiveSmallIntegerField(choices=[(1, 'FIRST_PLAYER_NAME'), (2, 'SECOND_PLAYER_NAME'), (3, 'THIRD_PLAYER_NAME'), (4, 'FOURTH_PLAYER_NAME')], default=1)),
                ('total_moves', models.PositiveSmallIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('deck', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hands', to='game.Deck')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='hand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='game.Hand'),
        ),
    ]
