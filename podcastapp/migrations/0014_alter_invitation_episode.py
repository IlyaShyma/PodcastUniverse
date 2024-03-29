# Generated by Django 4.1.3 on 2023-01-29 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("podcastapp", "0013_rename_to_user_user_profile_invitation_to_user_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invitation",
            name="episode",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="podcastapp.episode",
            ),
        ),
    ]
