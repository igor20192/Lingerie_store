import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from shop_api.views import (
    ProductListAPIView,
    ProductDetailAPIView,
)
from womanshop.models import (
    Product,
    Brand,
    Category,
    Style,
    Color,
    Size,
    ProductVariant,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class ProductAPITests(TestCase):
    """
    Tests for API views related to products.
    """

    def setUp(self):
        """
        Set up initial data for tests.
        """
        self.factory = APIRequestFactory()
        self.brand = Brand.objects.create(name="AVELIN")
        self.category = Category.objects.create(name="bodysuit")
        self.style = Style.objects.create(name="sexual")
        self.color = Color.objects.create(name="red")
        self.size = Size.objects.create(name="75C")

        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword"
        )
        self.client = APIClient()  # Создайте экземпляр APIClient
        self.client.force_authenticate(user=self.admin_user)

        self.not_admin_user = User.objects.create_user(
            username="not_admin",
            email="not_admin@example.com",
            password="notadminpassword",
        )
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.not_admin_user)

        self.url = "/api/products/create/"

    @staticmethod
    def create_image():
        image = Image.new("RGB", (100, 100), color="red")
        image_file = io.BytesIO()
        image.save(image_file, format="JPEG")
        image_name = "test_image.jpg"
        return SimpleUploadedFile(image_name, image_file.getvalue())

    def test_product_list_view(self):
        """
        Test for the product list view.
        """
        view = ProductListAPIView.as_view()
        request = self.factory.get("/api/products/")
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        """
        Test for the product detail view.
        """
        brand = get_object_or_404(Brand, id=self.brand.id)
        category = get_object_or_404(Category, id=self.category.id)
        style = get_object_or_404(Style, id=self.style.id)
        product = Product.objects.create(
            name="Test Product",
            price=99.99,
            brand=brand,
            category=category,
            style=style,
            sale=False,
            vendor_code="116182",
            collection="Classic",
        )
        view = ProductDetailAPIView.as_view()
        request = self.factory.get(f"/api/products/{product.pk}/")
        response = view(request, pk=product.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("name"), "Test Product")
        self.assertEqual(Product.objects.get().name, "Test Product")

    def test_create_product_as_admin(self):
        data = {
            "name": "Test Product",
            "price": 99.99,
            "brand": "/api/brand/1/",
            "category": "/api/categories/1/",
            "style": "/api/style/1/",
            "sale": False,
            "vendor_code": "admin",
            "collection": "Classic",
            "description": "description",
            "image1": self.create_image(),
            "image2": self.create_image(),
            "image3": self.create_image(),
            "image4": self.create_image(),
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, "Test Product")

    def test_create_product_as_non_admin(self):
        data = {
            "name": "Test Product1",
            "price": 99.99,
            "brand": "/api/brand/1/",
            "category": "/api/categories/1/",
            "style": "/api/style/1/",
            "sale": False,
            "vendor_code": "notadmin",
            "collection": "Classic",
            "description": "description",
            "image1": self.create_image(),
            "image2": self.create_image(),
            "image3": self.create_image(),
            "image4": self.create_image(),
        }

        response = self.client2.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 0)

    def test_product_variant_list_view_as_admin(self):
        response = self.client2.get("/api/product_variant/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_variant_list_view_as_not_admin(self):
        self.client2.logout()
        response = self.client2.get("/api/product_variant/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_variant_detail_view(self):
        self.client2.force_authenticate(user=self.not_admin_user)
        product = Product.objects.create(
            name="Test Product",
            price=99.99,
            brand=self.brand,
            category=self.category,
            style=self.style,
            sale=False,
            vendor_code="116181",
            collection="Classic",
        )

        product_variant = ProductVariant.objects.create(
            product=product,
            color=self.color,
            size=self.size,
        )

        response = self.client2.get(f"/api/product_variant/{product_variant.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, "Test Product")
        self.client2.logout()

        response2 = self.client2.get(f"/api/product_variant/{product_variant.pk}/")
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
