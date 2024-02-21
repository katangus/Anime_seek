# Generated by Django 4.1.1 on 2022-10-26 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("anime", "0015_alter_anime_anime"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="otaku",
            name="path_image",
        ),
        migrations.AlterField(
            model_name="anime",
            name="anime",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="anime",
            name="logo",
            field=models.CharField(default=None, max_length=500),
        ),
    ]
