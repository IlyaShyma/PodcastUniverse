# Generated by Django 4.1.3 on 2022-12-30 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("podcastapp", "0004_delete_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="podcast",
            name="creation_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
