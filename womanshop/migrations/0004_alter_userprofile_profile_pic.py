# Generated by Django 4.1.7 on 2023-04-08 07:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("womanshop", "0003_alter_userprofile_profile_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_pic",
            field=models.ImageField(blank=True, default=None, upload_to="profile_pics"),
        ),
    ]
