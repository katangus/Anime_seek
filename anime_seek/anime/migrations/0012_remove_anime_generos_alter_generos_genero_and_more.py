# Generated by Django 4.1.1 on 2022-10-24 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("anime", "0011_remove_anime_generos_anime_generos"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="anime",
            name="generos",
        ),
        migrations.AlterField(
            model_name="generos",
            name="genero",
            field=models.CharField(default=None, max_length=30, unique=True),
        ),
        migrations.AddField(
            model_name="anime",
            name="generos",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="anime.generos",
            ),
        ),
    ]