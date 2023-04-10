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
