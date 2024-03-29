# Generated by Django 4.1.3 on 2023-02-03 15:49

import audio_validator.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("podcastapp", "0016_comment_reports"),
    ]

    operations = [
        migrations.AlterField(
            model_name="episode",
            name="audio",
            field=models.FileField(
                null=True,
                upload_to="audio_files/",
                validators=[audio_validator.validator.AudioValidator("mp3")],
            ),
        ),
    ]
