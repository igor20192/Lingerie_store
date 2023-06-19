# Generated by Django 4.1.7 on 2023-06-11 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("womanshop", "0016_rename_quantity_product_stock"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="color",
        ),
        migrations.RemoveField(
            model_name="product",
            name="size",
        ),
        migrations.RemoveField(
            model_name="product",
            name="stock",
        ),
        migrations.CreateModel(
            name="ProductVariant",
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
                ("stock", models.PositiveIntegerField(default=1)),
                (
                    "color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="womanshop.color",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="womanshop.product",
                    ),
                ),
                (
                    "size",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="womanshop.size"
                    ),
                ),
            ],
        ),
    ]