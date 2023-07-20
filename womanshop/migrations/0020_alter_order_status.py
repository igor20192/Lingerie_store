# Generated by Django 4.1.7 on 2023-07-16 20:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("womanshop", "0019_alter_order_order_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("P", "Pending"),
                    ("O", "Order has been paid"),
                    ("C", "Confirmed"),
                    ("S", "Shipped"),
                    ("D", "Delivered"),
                ],
                max_length=1,
            ),
        ),
    ]
