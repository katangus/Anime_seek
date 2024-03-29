# Generated by Django 4.1.1 on 2022-10-20 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("anime", "0002_generos_anime"),
    ]

    operations = [
        migrations.RenameField(
            model_name="otaku",
            old_name="path",
            new_name="path_image",
        ),
        migrations.RemoveField(
            model_name="anime",
            name="nome",
        ),
        migrations.AddField(
            model_name="anime",
            name="anime",
            field=models.CharField(default=None, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="anime",
            name="trailer",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name="generos",
            name="genero",
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comentario", models.CharField(max_length=200)),
                ("pub_data", models.DateTimeField(verbose_name="data de publicacao")),
                (
                    "anime",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="anime.anime"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="List",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("watch", models.BooleanField(default=False)),
                (
                    "anime",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="anime.anime"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Friends",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "current_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("users", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
