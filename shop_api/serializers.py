from rest_framework import serializers
from womanshop.models import (
    UserProfile,
    Order,
    Category,
    Style,
    Brand,
    Color,
    Size,
    Product,
    ProductVariant,
    OrderItem,
)
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for User model.
    """

    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for UserProfile model.
    """

    class Meta:
        model = UserProfile
        fields = "__all__"


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Order model.
    """

    class Meta:
        model = Order
        fields = "__all__"


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Category model.
    """

    class Meta:
        model = Category
        fields = "__all__"


class StyleSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Style model.
    """

    class Meta:
        model = Style
        fields = "__all__"


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Brand model.
    """

    class Meta:
        model = Brand
        fields = "__all__"


class ColorSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Color model.
    """

    class Meta:
        model = Color
        fields = "__all__"


class SizeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Size model.
    """

    class Meta:
        model = Size
        fields = "__all__"


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Product model.
    """

    class Meta:
        model = Product
        fields = "__all__"
        view_name = "product-detail"


class ProductVariantSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ProductVariant model.
    """

    class Meta:
        model = ProductVariant
        fields = "__all__"


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for OrderItem model.
    """

    class Meta:
        model = OrderItem
        fields = "__all__"
