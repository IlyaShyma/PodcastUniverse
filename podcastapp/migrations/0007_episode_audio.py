# Generated by Django 4.1.3 on 2023-01-25 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("podcastapp", "0006_alter_episode_creation_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="episode",
            name="audio",
            field=models.FileField(null=True, upload_to="audio_files/"),
        ),
    ]