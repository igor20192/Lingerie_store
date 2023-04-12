from django.contrib import admin
from .models import UserProfile, Order, Category, Style, Brand, Size, Color, Product

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Style)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product)
