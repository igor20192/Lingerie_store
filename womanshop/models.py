from django.db import models
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # поля профиля
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True, default="active")
    zip_code = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.CharField(
        max_length=1, choices=(("M", "Male"), ("F", "Female")), null=True
    )
    # поля для фотографии профиля
    profile_pic = models.ImageField(
        upload_to="profile_pics/", blank=True, default="profile_pics/not_photo.png"
    )

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # поля заказа
    order_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=8, decimal_places=2)
    # поля для статуса заказа
    STATUS_CHOICES = (
        ("P", "Pending"),
        ("C", "Confirmed"),
        ("S", "Shipped"),
        ("D", "Delivered"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.order_number


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Style(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    upload_to = "products/"

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
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
