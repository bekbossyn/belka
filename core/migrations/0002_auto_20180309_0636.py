# Generated by Django 2.0 on 2018-03-09 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokenlog',
            name='deleted',
        ),
        migrations.AddField(
            model_name='tokenlog',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
