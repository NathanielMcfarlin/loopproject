# Generated by Django 4.2.9 on 2024-01-09 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loopapi', '0003_game_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_image_url',
            field=models.URLField(max_length=5000),
        ),
    ]
