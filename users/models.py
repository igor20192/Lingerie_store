from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class UserProfile(models.Model):
    """
    Model representing a user profile.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True, default="active")
    zip_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.CharField(
        max_length=1, choices=(("M", "Male"), ("F", "Female")), blank=True
    )
    profile_pic = models.ImageField(
        upload_to="profile_pics/", blank=True, default="profile_pics/not_photo.png"
    )

    def __str__(self):
        return self.user.username
