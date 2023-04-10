# Generated by Django 4.1.7 on 2023-04-09 13:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("womanshop", "0006_alter_userprofile_profile_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_pic",
            field=models.ImageField(
                blank=True,
                default="profile_pics/not_photo.png",
                upload_to="profile_pics",
            ),
        ),
    ]