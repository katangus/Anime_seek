# Generated by Django 4.1.1 on 2022-10-24 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("anime", "0014_remove_anime_trailer_alter_anime_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anime",
            name="anime",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
