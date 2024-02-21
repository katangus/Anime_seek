# Generated by Django 4.1.1 on 2022-10-21 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("anime", "0003_rename_path_otaku_path_image_remove_anime_nome_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="friends",
            name="current_user",
        ),
        migrations.RemoveField(
            model_name="friends",
            name="users",
        ),
        migrations.AddField(
            model_name="friends",
            name="friends",
            field=models.ManyToManyField(
                blank=True, related_name="friends", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="friends",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]