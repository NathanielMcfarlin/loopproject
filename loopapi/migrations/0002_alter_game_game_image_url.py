# Generated by Django 4.2.9 on 2024-01-09 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loopapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_image_url',
            field=models.URLField(max_length=1000),
        ),
    ]
