# Generated by Django 4.1.7 on 2023-04-03 19:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                ("address", models.CharField(max_length=255, null=True)),
                ("city", models.CharField(max_length=255, null=True)),
                ("state", models.CharField(max_length=255, null=True)),
                ("zip_code", models.CharField(max_length=10, null=True)),
                ("phone_number", models.CharField(max_length=20, null=True)),
                ("date_of_birth", models.DateField(default=datetime.date.today)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")],
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "profile_pic",
                    models.ImageField(blank=True, upload_to="profile_pics"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                ("order_number", models.CharField(max_length=20, unique=True)),
                ("order_date", models.DateTimeField(auto_now_add=True)),
                ("order_total", models.DecimalField(decimal_places=2, max_digits=8)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Pending"),
                            ("C", "Confirmed"),
                            ("S", "Shipped"),
                            ("D", "Delivered"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="womanshop.userprofile",
                    ),
                ),
            ],
        ),
    ]
