import sys
from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User
import datetime
from decimal import Decimal
from users.models import UserProfile


class Order(models.Model):
    """
    Model representing an order.
    """

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=24, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=8, decimal_places=2)

    STATUS_CHOICES = (
        ("P", "Pending"),
        ("O", "Order has been paid"),
        ("C", "Confirmed"),
        ("S", "Shipped"),
        ("D", "Delivered"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.order_number


class Category(models.Model):
    """
    Model representing a product category.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Style(models.Model):
    """
    Model representing a product style.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Model representing a brand.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    """
    Model representing a color.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Size(models.Model):
    """
    Model representing a size.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Model representing a product.
    """

    upload_to = "products/"

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    vendor_code = models.CharField(max_length=6, unique=True)
    collection = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image1 = models.ImageField(upload_to=upload_to)
    image2 = models.ImageField(upload_to=upload_to)
    image3 = models.ImageField(upload_to=upload_to)
    image4 = models.ImageField(upload_to=upload_to)
    sale = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """
    Model representing a product variant.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - Color: {self.color.name}, Size: {self.size.name}"


class OrderItem(models.Model):
    """
    Model representing an item in an order.
    """

    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product_variant.product.name} - {self.quantity} - order_number:{self.order.order_number}"

    def save(self, *args, **kwargs):
        self.price = self.product_variant.product.price
        quantity = Decimal(self.quantity)

        if "test" in sys.argv:
            quantity = self.quantity

        self.subtotal = self.product_variant.product.price * quantity
        return super().save(*args, **kwargs)
