import base64
import os
import io
import json
from random import randint
from decimal import Decimal
from PIL import Image
from django.urls import reverse
from django.test import TestCase
from io import BytesIO
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.test import APIClient, APIRequestFactory
from shop_api.serializers import (
    UserSerializer,
    UserProfileSerializer,
    OrderSerializer,
    CategorySerializer,
    StyleSerializer,
    BrandSerializer,
    ColorSerializer,
    SizeSerializer,
    ProductSerializer,
    ProductVariantSerializer,
    OrderItemSerializer,
)
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


class UserSerializerTest(TestCase):
    """
    The class to test the UserSerializer.

    Attributes:
    - factory: APIRequestFactory instance for making requests
    - user_data: user data to instantiate User
    - user: instance of the created user
    - serializer: UserSerializer instance to test
    - userprofile_data: user profile data to instantiate UserProfile
    - userprofile: an instance of the generated user profile
    - userprofile_serializer: UserProfileSerializer instance for testing
    - order_data: order data to instantiate Order
    - order: an instance of the created order
    - order_serializer: OrderSerializer instance to test
    - categories_data: Category data to instantiate Category
    - categories: an instance of the created category
    - categories_serializer: CategorySerializer instance to test
    - style_data: style data to instantiate the Style
    - style: an instance of the generated style
    - style_serialiser: StyleSerializer instance to test
    - brand_data: Brand data to instantiate Brand
    - brand: an instance of the created brand
    - brand_serializer: BrandSerializer instance to test
    - color_data: color data to instantiate Color
    - color: an instance of the created color
    - color_serializer: ColorSerializer instance to test
    - size_data: size data to instantiate Size
    - size: an instance of the created size
    - size_serializer: SizeSerializer instance to test
    - product_data: product data to instantiate Product
    - product: an instance of the created product
    - product_serializer: ProductSerializer instance to test
    - product_variant_data: product variant data to instantiate ProductVariant
    - product_variant: an instance of the generated product variant
    - product_variant_serializer: ProductVariantSerializer instance for testing
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "testpassword",
        }

        self.user = User.objects.create(**self.user_data)
        url = reverse("user-detail", args=[self.user.id])
        request = self.factory.get(url)
        self.serializer = UserSerializer(
            context={"request": request}, instance=self.user
        )

        self.userprofile_data = {
            "user": self.user,
            "address": "Via Callicratide 9",
            "city": "La Saxe",
            "state": "Aosta",
            "zip_code": "11013",
            "phone_number": "0337 6083509",
            "gender": "F",
        }
        self.userprofile = UserProfile.objects.create(**self.userprofile_data)
        url_userprofile = reverse("userprofile-detail", args=[self.userprofile.id])
        request_userprofile = self.factory.get(url_userprofile)
        self.userprofile_serializer = UserProfileSerializer(
            context={"request": request_userprofile}, instance=self.userprofile
        )

        self.order_data = {
            "user_profile": self.userprofile,
            "order_number": str(randint(100000, 999999)),
            "order_total": "100.00",
            "status": "P",
        }
        self.order = Order.objects.create(**self.order_data)
        url_order = reverse("order-detail", args=[self.order.pk])
        request_order = self.factory.get(url_order)
        self.order_serializer = OrderSerializer(
            context={"request": request_order}, instance=self.order
        )

        self.categories_data = {"name": "bras"}
        self.categories = Category.objects.create(**self.categories_data)
        url_categories = reverse("category-detail", args=[self.categories.pk])
        request_categories = self.factory.get(url_categories)
        self.categories_serializer = CategorySerializer(
            context={"request": request_categories}, instance=self.categories
        )

        self.style_data = {"name": "sexual"}
        self.style = Style.objects.create(**self.style_data)
        url_style = reverse("style-detail", args=[self.style.pk])
        request_style = self.factory.get(url_style)
        self.style_serialiser = StyleSerializer(
            context={"request": request_style}, instance=self.style
        )

        self.brand_data = {"name": "AVELIN"}
        self.brand = Brand.objects.create(**self.brand_data)
        url_brand = reverse("brand-detail", args=[self.brand.pk])
        request_brand = self.factory.get(url_brand)
        self.brand_serializer = BrandSerializer(
            context={"request": request_brand}, instance=self.brand
        )

        self.color_data = {"name": "red"}
        self.color = Color.objects.create(**self.color_data)
        url_color = reverse("color-detail", args=[self.color.pk])
        request_color = self.factory.get(url_color)
        self.color_serializer = ColorSerializer(
            context={"request": request_color}, instance=self.color
        )

        self.size_data = {"name": "80B"}
        self.size = Size.objects.create(**self.size_data)
        url_size = reverse("size-detail", args=[self.size.pk])
        request_size = self.factory.get(url_size)
        self.size_serializer = SizeSerializer(
            context={"request": request_size}, instance=self.size
        )

        self.product_data = {
            "name": "Бюстгальтер балконет (Classic)",
            "category": self.categories,
            "style": self.style,
            "brand": self.brand,
            "vendor_code": "111111",
            "collection": "Classic",
            "price": "111.00",
            "description": "description",
            "sale": False,
        }
        self.product = Product.objects.create(**self.product_data)
        url_product = reverse("product-detail", args=[self.product.pk])
        request_product = self.factory.get(url_product)
        self.product_serializer = ProductSerializer(
            context={"request": request_product}, instance=self.product
        )

        self.product_vriant_data = {
            "product": self.product,
            "color": self.color,
            "size": self.size,
            "stock": 3,
        }
        self.product_variant = ProductVariant.objects.create(**self.product_vriant_data)
        url_product_variant = reverse(
            "productvariant-detail", args=[self.product_variant.pk]
        )
        request_product_variant = self.factory.get(url_product_variant)
        self.product_variant_serializer = ProductVariantSerializer(
            context={"request": request_product_variant}, instance=self.product_variant
        )

        self.order_item_data = {
            "order": self.order,
            "product_variant": self.product_variant,
        }
        self.order_item = OrderItem.objects.create(**self.order_item_data)
        url_order_item = reverse("orderitem-detail", args=[self.order_item.pk])
        request_order_item = self.factory.get(url_order_item)
        self.order_item_serializer = OrderItemSerializer(
            context={"request": request_order_item}, instance=self.order_item
        )

    @staticmethod
    def create_image():
        image = Image.new("RGB", (100, 100), color="red")
        image_file = io.BytesIO()
        image.save(image_file, format="JPEG")
        image_name = "test_image.jpg"
        return SimpleUploadedFile(image_name, image_file.getvalue())

    def test_user_serializer_contains_expected_fields(self):
        """
        Test that the serialized data contains all the expected fields.
        """
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "is_superuser",
                    "password",
                    "groups",
                    "is_active",
                    "user_permissions",
                    "url",
                    "last_login",
                    "date_joined",
                    "is_staff",
                ]
            ),
        )

    def test_user_serializer_data_matches_user_data(self):
        """
        Test that the serialized data matches the user data.
        """
        data = self.serializer.data
        self.assertEqual(data["username"], self.user_data["username"])
        self.assertEqual(data["first_name"], self.user_data["first_name"])
        self.assertEqual(data["last_name"], self.user_data["last_name"])
        self.assertEqual(data["email"], self.user_data["email"])

    def test_user_serializer_json_rendering(self):
        """
        Test the JSON rendering of the user serializer.
        """
        serialized_data = json.loads(json.dumps(self.serializer.data))

        expected_data = {
            "url": f"http://testserver/api/user/{self.user.pk}/",
            "password": "testpassword",
            "last_login": None,
            "is_superuser": False,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": serialized_data["date_joined"],
            "groups": [],
            "user_permissions": [],
        }

        self.assertEqual(serialized_data, expected_data)

    def test_user_serializer_json_parsing(self):
        """
        Test the JSON parsing of the user serializer.
        """
        expected_data = {
            "url": f"http://testserver/api/user/{self.user.pk}/",
            "password": "newtestpassword",
            "last_login": None,
            "is_superuser": False,
            "username": "newtestuser",
            "first_name": "NewTest",
            "last_name": "NewUser",
            "email": "newtest@example.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2023-08-27T15:24:47.008580Z",
        }

        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = UserSerializer(data=parsed_data)

        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "newtestuser")
        self.assertEqual(user.first_name, "NewTest")
        self.assertEqual(user.last_name, "NewUser")
        self.assertEqual(user.email, "newtest@example.com")

    def test_userprofile_serializer_contains_expected_fields(self):
        """
        Test that the UserProfileSerializer contains the expected fields.
        """
        data = self.userprofile_serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "url",
                    "user",
                    "address",
                    "city",
                    "state",
                    "zip_code",
                    "phone_number",
                    "date_of_birth",
                    "gender",
                    "profile_pic",
                ]
            ),
        )

    def test_userprofile_serializer_data_matches_userprofile_data(self):
        """
        Test that the data returned by the UserProfileSerializer matches the expected UserProfile data.
        """
        data = self.userprofile_serializer.data
        self.assertEqual(data["address"], self.userprofile_data["address"])
        self.assertEqual(data["city"], self.userprofile_data["city"])
        self.assertEqual(data["state"], self.userprofile_data["state"])
        self.assertEqual(data["zip_code"], self.userprofile_data["zip_code"])
        self.assertEqual(data["phone_number"], self.userprofile_data["phone_number"])
        self.assertEqual(data["gender"], self.userprofile_data["gender"])

    def test_userprofile_serializer_json_rendering(self):
        """
        Test that the UserProfileSerializer correctly renders JSON data.
        """
        serializer_data = json.loads(json.dumps(self.userprofile_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/user_profile/{self.userprofile.pk}/",
            "user": f"http://testserver/api/user/{self.user.pk}/",
            "address": "Via Callicratide 9",
            "city": "La Saxe",
            "state": "Aosta",
            "zip_code": "11013",
            "phone_number": "0337 6083509",
            "date_of_birth": serializer_data["date_of_birth"],
            "gender": "F",
            "profile_pic": "http://testserver/media/profile_pics/not_photo.png",
        }
        self.assertEqual(serializer_data, expected_data)

    def test_userprofile_serializer_json_parsing(self):
        """
        Test that the UserProfileSerializer correctly parses JSON data.
        """
        user_data = {
            "username": "newtestuser2",
            "first_name": "NewTest",
            "last_name": "NewUser",
            "email": "newtest2@example.com",
            "password": "newtestpassword",
        }
        user = User.objects.create(**user_data)
        profile_data = {
            "user": user,
            "address": "Via Callicratide 9",
            "city": "La Saxe",
            "state": "Aosta",
            "zip_code": "11013",
            "phone_number": "0337 6083509",
            "gender": "F",
        }
        expected_data = {
            "url": "http://testserver/api/user_profile/2/",
            "user": f"http://testserver/api/user/{user.pk}/",
            "address": "Via Callicratide 10",
            "city": "La Saxe",
            "state": "Aosta",
            "zip_code": "11014",
            "phone_number": "0337 6083509",
            "gender": "F",
            # "profile_pic": "http://testserver/media/profile_pics/not_photo.png",
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = UserProfileSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        userprofile = serializer.save()
        self.assertEqual(userprofile.address, "Via Callicratide 10")
        self.assertEqual(userprofile.city, "La Saxe")
        self.assertEqual(userprofile.state, "Aosta")
        self.assertEquals(userprofile.zip_code, "11014")
        self.assertEqual(userprofile.phone_number, "0337 6083509")
        self.assertEqual(userprofile.gender, "F")

    def test_order_serializer_contains_expected_fields(self):
        """
        Test if the order serializer contains the expected fields.
        """
        data = self.order_serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "user_profile",
                    "order_number",
                    "order_total",
                    "status",
                    "order_date",
                    "url",
                ]
            ),
        )

    def test_order_serializer_data_matches_order_data(self):
        """
        Test if the data in the order serializer matches the order data.
        """
        data = self.order_serializer.data
        self.assertEqual(data["order_number"], self.order_data["order_number"])
        self.assertEqual(data["order_total"], self.order_data["order_total"])
        self.assertEqual(data["status"], self.order_data["status"])
        self.assertEqual(
            data["user_profile"], f"http://testserver/api/user_profile/{self.order.pk}/"
        )

    def test_order_serializer_json_rendering(self):
        """
        Test the JSON rendering of the order serializer.
        """
        serialized_data = json.loads(json.dumps(self.order_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/orders/{self.order.pk}/",
            "user_profile": f"http://testserver/api/user_profile/{self.userprofile.pk}/",
            "order_number": serialized_data["order_number"],
            "order_total": "100.00",
            "order_date": serialized_data["order_date"],
            "status": "P",
        }
        self.assertEqual(serialized_data, expected_data)

    def test_order_serializer_json_parsing(self):
        """
        Test the JSON parsing of the order serializer.
        """
        user_data = {
            "username": "testuser_order",
            "first_name": "TestOrder",
            "last_name": "UserOrder",
            "email": "testorder@example.com",
            "password": "testorderpassword",
        }
        user = User.objects.create(**user_data)

        profile_data = {
            "user": user,
            "address": "Via Callicratide 19",
            "city": "La Saxe",
            "state": "Aosta",
            "zip_code": "11010",
            "phone_number": "0337 6083500",
            "gender": "F",
        }
        profile = UserProfile.objects.create(**profile_data)

        expected_data = {
            "url": "http://testserver/api/orders/2/",
            "user_profile": f"http://testserver/api/user_profile/{profile.pk}/",
            "order_number": "999999",
            "order_total": "101.00",
            "status": "P",
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = OrderSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.order_number, "999999")
        self.assertEqual(order.order_total, Decimal("101"))
        self.assertEqual(order.status, "P")

    def test_categories_serializer_contains_expected_fields(self):
        """
        Test that the categories serializer contains the expected fields.
        """
        data = self.categories_serializer.data
        self.assertEqual(set(data.keys()), set(["url", "name"]))

    def test_categories_serializer_data_matches_categories_data(self):
        """
        Test that the data in the categories serializer matches the expected categories data.
        """
        data = self.categories_serializer.data
        self.assertEqual(data["name"], self.categories_data["name"])

    def test_categories_serializer_json_rendering(self):
        """
        Test the JSON rendering of the categories serializer.
        """
        serialized_data = json.loads(json.dumps(self.categories_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/categories/{self.categories.pk}/",
            "name": "bras",
        }
        self.assertEqual(serialized_data, expected_data)

    def test_categories_serializer_json_parsing(self):
        """
        Test the JSON parsing of the categories serializer.
        """
        expected_data = {
            "url": "http://testserver/api/categories/2/",
            "name": "panties",
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = CategorySerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        categories = serializer.save()
        self.assertEqual(categories.name, "panties")

    def test_style_serializer_contains_expected_fields(self):
        """
        Test that the style serializer contains the expected fields.
        """
        data = self.style_serialiser.data
        self.assertEqual(set(data.keys()), set(["url", "name"]))

    def test_style_serializer_data_matches_style_data(self):
        """
        Test that the data in the style serializer matches the expected style data.
        """
        data = self.style_serialiser.data
        self.assertEqual(data["name"], self.style_data["name"])

    def test_style_serializer_json_rendering(self):
        """
        Test the JSON rendering of the style serializer.
        """
        serialized_data = json.loads(json.dumps(self.style_serialiser.data))
        expected_data = {
            "url": f"http://testserver/api/style/{self.style.pk}/",
            "name": "sexual",
        }
        self.assertEqual(serialized_data, expected_data)

    def test_style_serializer_json_parsing(self):
        """
        Test the JSON parsing of the style serializer.
        """
        expected_data = {
            "url": "http://testserver/api/style/2/",
            "name": "lacy",
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = StyleSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        style = serializer.save()
        self.assertEqual(style.name, "lacy")

    def test_brand_serializer_contains_expected_fields(self):
        """
        Test that the brand serializer contains the expected fields.
        """
        data = self.brand_serializer.data
        self.assertEqual(set(data.keys()), set(["url", "name"]))

    def test_brand_serializer_data_matches_brand_data(self):
        """
        Test that the data returned by the brand serializer matches the brand data.
        """
        data = self.brand_serializer.data
        self.assertEqual(data["name"], self.brand_data["name"])

    def test_brand_serializer_json_rendering(self):
        """
        Test the JSON rendering of the brand serializer.
        """
        serialized_data = json.loads(json.dumps(self.brand_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/brand/{self.brand.pk}/",
            "name": "AVELIN",
        }
        self.assertEqual(serialized_data, expected_data)

    def test_brand_serializer_json_parsing(self):
        """
        Test the JSON parsing of the brand serializer.
        """
        expected_data = {
            "url": "http://testserver/api/brand/2/",
            "name": "LAUMA",
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = BrandSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        brand = serializer.save()
        self.assertEqual(brand.name, "LAUMA")

    def test_color_serializer_contains_expected_fields(self):
        """
        Test that the color serializer contains the expected fields.
        """
        data = self.color_serializer.data
        self.assertEqual(set(data.keys()), set(["url", "name"]))

    def test_color_serializer_data_matches_color_data(self):
        """
        Test that the data returned by the color serializer matches the color data.
        """
        data = self.color_serializer.data
        self.assertEqual(data["name"], self.color_data["name"])

    def test_color_serializer_json_rendering(self):
        """
        Test the JSON rendering of the color serializer.
        """
        serialized_data = json.loads(json.dumps(self.color_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/color/{self.color.pk}/",
            "name": "red",
        }
        self.assertEqual(serialized_data, expected_data)

    def test_color_serializer_json_parsing(self):
        """
        Test the JSON parsing of the color serializer.
        """
        expected_data = {
            "url": "http://testserver/api/color/2/",
            "name": "blue",
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = ColorSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        color = serializer.save()
        self.assertEqual(color.name, "blue")

    def test_size_serializer_contains_expected_fields(self):
        """
        Test that the size serializer contains the expected fields.
        """
        data = self.size_serializer.data
        self.assertEqual(set(data.keys()), set(["url", "name"]))

    def test_size_serializer_data_matches_size_data(self):
        """
        Test that the data returned by the size serializer matches the size data.
        """
        data = self.size_serializer.data
        self.assertEqual(data["name"], self.size_data["name"])

    def test_sise_serializer_json_rendering(self):
        """
        Test the JSON rendering of the size serializer.
        """
        serialized_data = json.loads(json.dumps(self.size_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/size/{self.size.pk}/",
            "name": "80B",
        }
        self.assertEqual(serialized_data, expected_data)

    def test_size_serializer_json_parsing(self):
        """
        Test the JSON parsing of the size serializer.
        """
        expected_data = {
            "url": "http://testserver/api/size/2/",
            "name": "80C",
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = SizeSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        size = serializer.save()
        self.assertEqual(size.name, "80C")

    def test_product_serializer_contains_expected_fields(self):
        """
        Test that the product serializer contains the expected fields.

        Asserts that the serialized data contains all the expected fields:
        - "url"
        - "name"
        - "category"
        - "style"
        - "brand"
        - "vendor_code"
        - "collection"
        - "price"
        - "description"
        - "sale"
        - "created_at"
        - "image1"
        - "image2"
        - "image3"
        - "image4"
        """
        data = self.product_serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "url",
                    "name",
                    "category",
                    "style",
                    "brand",
                    "vendor_code",
                    "collection",
                    "price",
                    "description",
                    "sale",
                    "created_at",
                    "image1",
                    "image2",
                    "image3",
                    "image4",
                ]
            ),
        )

    def test_product_serializer_data_matches_product_data(self):
        """
        Test that the product serializer data matches the product data.

        Asserts that the serialized data matches the expected product data:
        - "name"
        - "vendor_code"
        - "collection"
        - "price"
        - "description"
        - "sale"
        - "category"
        - "style"
        - "brand"
        """
        data = self.product_serializer.data
        self.assertEqual(data["name"], self.product_data["name"])
        self.assertEqual(data["vendor_code"], self.product_data["vendor_code"])
        self.assertEqual(data["collection"], self.product_data["collection"])
        self.assertEqual(data["price"], self.product_data["price"])
        self.assertEqual(data["description"], self.product_data["description"])
        self.assertEqual(data["sale"], self.product_data["sale"])
        self.assertEqual(
            data["category"], f"http://testserver/api/categories/{self.categories.pk}/"
        )
        self.assertEqual(data["style"], f"http://testserver/api/style/{self.style.pk}/")
        self.assertEqual(data["brand"], f"http://testserver/api/brand/{self.brand.pk}/")

    def test_product_serializer_json_rendering(self):
        """
        Test the JSON rendering of the product serializer data.

        Serializes the data and compares it to the expected JSON representation.
        Asserts that the serialized data matches the expected JSON data.
        """
        serialized_data = json.loads(json.dumps(self.product_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/products/{self.product.pk}/",
            "name": "Бюстгальтер балконет (Classic)",
            "category": f"http://testserver/api/categories/{self.categories.pk}/",
            "style": f"http://testserver/api/style/{self.style.pk}/",
            "brand": f"http://testserver/api/brand/{self.brand.pk}/",
            "vendor_code": "111111",
            "collection": "Classic",
            "price": "111.00",
            "description": "description",
            "sale": False,
            "created_at": self.product_serializer.data["created_at"],
            "image1": self.product_serializer.data["image1"],
            "image2": self.product_serializer.data["image2"],
            "image3": self.product_serializer.data["image3"],
            "image4": self.product_serializer.data["image4"],
        }
        self.assertEqual(serialized_data, expected_data)

    def test_product_serializer_json_parsing(self):
        """
        Test the JSON parsing of the product serializer data.

        Creates a JSON representation of the expected data and parses it using the serializer.
        Asserts that the parsed data matches the expected data.
        """
        expected_data = {
            "url": reverse("product-detail", args=[2]),
            "name": "Бюстгальтер (Classic)",
            "category": reverse("category-detail", args=[self.categories.pk]),
            "style": reverse("style-detail", args=[self.style.pk]),
            "brand": reverse("brand-detail", args=[self.brand.pk]),
            "vendor_code": "222222",
            "collection": "Classic",
            "price": "222.00",
            "description": "newdescription",
            "sale": False,
            "image1": self.create_image(),
            "image2": self.create_image(),
            "image3": self.create_image(),
            "image4": self.create_image(),
        }
        serializer = ProductSerializer(data=expected_data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.name, "Бюстгальтер (Classic)")
        self.assertEqual(product.vendor_code, "222222")
        self.assertEqual(product.collection, "Classic")
        self.assertEqual(product.price, Decimal("222.00"))
        self.assertEqual(product.description, "newdescription")
        self.assertFalse(product.sale)

    def test_product_variant_serializer_contains_expected_fields(self):
        """
        Test that the product variant serializer contains the expected fields.
        """
        data = self.product_variant_serializer.data
        self.assertEqual(
            set(data.keys()), set(["url", "product", "color", "size", "stock"])
        )

    def test_product_variant_serializer_data_matches_product_variant_data(self):
        """
        Test that the data in the product variant serializer matches the product variant data.
        """
        data = self.product_variant_serializer.data
        self.assertEqual(data["stock"], self.product_vriant_data["stock"])
        self.assertEqual(
            data["url"],
            f"http://testserver/api/product_variant/{self.product_variant.pk}/",
        )
        self.assertEqual(
            data["product"], f"http://testserver/api/products/{self.product.pk}/"
        )
        self.assertEqual(data["color"], f"http://testserver/api/color/{self.color.pk}/")
        self.assertEqual(data["size"], f"http://testserver/api/size/{self.size.pk}/")

    def test_product_variant_serializer_json_rendering(self):
        """
        Test the JSON rendering of the product variant serializer.
        """
        serialized_data = json.loads(json.dumps(self.product_variant_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/product_variant/{self.product_variant.pk}/",
            "product": f"http://testserver/api/products/{self.product.pk}/",
            "color": f"http://testserver/api/color/{self.color.pk}/",
            "size": f"http://testserver/api/size/{self.size.pk}/",
            "stock": 3,
        }
        self.assertEqual(serialized_data, expected_data)

    def test_product_variant_serializer_json_parsing(self):
        """
        Test the JSON parsing of the product variant serializer.
        """
        expected_data = {
            "url": "http://testserver/api/product_variant/2/",
            "product": f"http://testserver/api/products/{self.product.pk}/",
            "color": f"http://testserver/api/color/{self.color.pk}/",
            "size": f"http://testserver/api/size/{self.size.pk}/",
            "stock": 33,
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = ProductVariantSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        product_variant = serializer.save()
        self.assertEqual(product_variant.stock, 33)
        self.assertEqual(product_variant.product.name, "Бюстгальтер балконет (Classic)")
        self.assertEqual(product_variant.color.name, "red")
        self.assertEqual(product_variant.size.name, "80B")

    def test_orderitem_serializer_contains_expected_fields(self):
        """
        Checks if the OrderItemSerializer contains the expected fields.
        """
        data = self.order_item_serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["url", "order", "product_variant", "quantity", "price", "subtotal"]),
        )

    def test_orderitem_serializer_data_matches_orderitem_data(self):
        """
        Checks if the data of the OrderItemSerializer matches the data of the OrderItem.
        """
        data = self.order_item_serializer.data
        self.assertEqual(
            data["url"], f"http://testserver/api/orders_item/{self.order_item.pk}/"
        )
        self.assertEqual(
            data["order"], f"http://testserver/api/orders/{self.order.pk}/"
        )
        self.assertEqual(data["quantity"], 1)
        self.assertEqual(data["price"], "111.00")
        self.assertEqual(data["subtotal"], "111.00")

    def test_orderitem_serializer_json_rendering(self):
        """
        Checks if the OrderItemSerializer data is serialized correctly to JSON.
        """
        serialized_data = json.loads(json.dumps(self.order_item_serializer.data))
        expected_data = {
            "url": f"http://testserver/api/orders_item/{self.order_item.pk}/",
            "order": f"http://testserver/api/orders/{self.order.pk}/",
            "product_variant": f"http://testserver/api/product_variant/{self.product_variant.pk}/",
            "quantity": 1,
            "price": "111.00",
            "subtotal": "111.00",
        }
        self.assertEqual(serialized_data, expected_data)

    def test_orderitem_serializer_json_parsing(self):
        """
        Checks if JSON data is parsed correctly in the OrderItemSerializer.
        """
        expected_data = {
            "url": "http://testserver/api/orders_item/2/",
            "order": f"http://testserver/api/orders/{self.order.pk}/",
            "product_variant": f"http://testserver/api/product_variant/{self.product_variant.pk}/",
            "quantity": 2,
            "price": "111.00",
            "subtotal": "222.00",
        }
        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = OrderItemSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        orderitem = serializer.save()
        self.assertEqual(orderitem.quantity, 2)
        self.assertEqual(str(orderitem.price), "111.00")
        self.assertEqual(str(orderitem.subtotal), "222.00")
        self.assertEqual(orderitem.order, self.order)
        self.assertEqual(orderitem.product_variant, self.product_variant)
