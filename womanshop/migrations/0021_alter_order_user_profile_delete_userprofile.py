# Generated by Django 4.1.7 on 2023-09-07 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("womanshop", "0020_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="user_profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.userprofile"
            ),
        ),
        migrations.DeleteModel(
            name="UserProfile",
        ),
    ]
