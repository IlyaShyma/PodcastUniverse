# Generated by Django 4.1.3 on 2023-02-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profileManagementApp", "0005_userprofile_following"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="profile_bio",
            field=models.CharField(max_length=150, null=True),
        ),
    ]