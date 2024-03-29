# Generated by Django 4.1.1 on 2022-10-24 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("anime", "0012_remove_anime_generos_alter_generos_genero_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anime",
            name="anime",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="anime",
            name="trailer",
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name="generos",
            name="genero",
            field=models.CharField(default=None, max_length=30),
        ),
    ]
