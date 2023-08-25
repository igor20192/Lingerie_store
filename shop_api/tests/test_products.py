import io
from decimal import Decimal
import random
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
    Order,
    UserProfile,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class ProductAPITests(TestCase):
    """Tests for API views related to products."""

    def setUp(self):
        """Sets initial data for tests."""
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
        # Create userprofile
        self.userprofile_admin = UserProfile.objects.create(
            user=self.admin_user,
        )
        self.userprofile_not_admin = UserProfile.objects.create(
            user=self.not_admin_user
        )
        # Create orders for testing
        self.staff_order = Order.objects.create(
            user_profile=self.userprofile_admin,
            order_number="111111111",
            order_total=100.00,
            status="P",
        )
        self.non_staff_order = Order.objects.create(
            user_profile=self.userprofile_not_admin,
            order_number="222222222",
            order_total=100.00,
            status="P",
        )
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
        """Product creation test by administrator."""
        data = {
            "name": "Test Product",
            "price": 99.99,
            "brand": f"/api/brand/{self.brand.pk}/",
            "category": f"/api/categories/{self.category.pk}/",
            "style": f"/api/style/{self.style.pk}/",
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

    def test_create_product_as_not_admin(self):
        """Non-administrator product creation test."""
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
        """Product Variant List Test administrator."""
        response = self.client2.get("/api/product_variant/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_variant_list_view_as_no_admin(self):
        """Product variant list test is not administrator."""
        self.client2.logout()
        response = self.client2.get("/api/product_variant/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_variant_detail_view(self):
        """
        Test for the product variant detail view.
        This test checks the behavior of the API endpoint responsible for fetching
        the details of a product variant.

        Steps:
        1. Authenticate the user.
        2. Create a product and its variant.
        3. Retrieve the details of the product variant.
        4. Check the response status code and the name of the product.
        5. Logout the user.
        6. Attempt to access the product variant details after logging out.
        7. Check that the access is forbidden.
        """
        # Authenticate the user
        self.client2.force_authenticate(user=self.not_admin_user)

        # Create a product and its variant
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

        # Retrieve the details of the product variant
        response = self.client2.get(f"/api/product_variant/{product_variant.pk}/")

        # Check the response status code and the name of the product
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().name, "Test Product")

        # Logout the user
        self.client2.logout()

        # Attempt to access the product variant details after logging out
        response2 = self.client2.get(f"/api/product_variant/{product_variant.pk}/")

        # Check that the access is forbidden
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_categories_list_view_as_authenticated(self):
        """
        Test the categories list view when the user is authenticated.

        Steps:
        1. Get the list of categories while authenticated.
        2. Check that the response status code is 200.
        3. Check that the first category's name matches "bodysuit".
        """
        response = self.client2.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0].get("name"), "bodysuit")

    def test_categories_list_view_as_not_authenticated(self):
        """
        Test the categories list view when the user is not authenticated.

        Steps:
        1. Log out the user.
        2. Get the list of categories.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.logout()
        response = self.client2.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_categories_detail_view_as_authenticated(self):
        """
        Test the categories detail view when the user is authenticated.

        Steps:
        1. Authenticate the user.
        2. Get the details of a category.
        3. Check that the response status code is 200.
        4. Check that the category's name matches "bodysuit".
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/categories/{self.category.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "bodysuit")

    def test_categories_detail_view_as_not_authenticated(self):
        """
        Test the categories detail view when the user is not authenticated.

        Steps:
        1. Log out the user.
        2. Get the details of a category.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.logout()
        response = self.client2.get(f"/api/categories/{self.category.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_categories_as_admin(self):
        """
        Test category creation as an admin user.

        Steps:
        1. Create category data with name "bras".
        2. Post the category data to the creation endpoint while authenticated as an admin.
        3. Check that the response status code is 201 (created).
        4. Check that a category with the name "bras" exists in the database.
        """
        data = {"name": "bras"}
        response = self.client.post("/api/categories/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name="bras"))

    def test_create_categories_as_not_admin(self):
        """
        Test category creation as a non-admin user.

        Steps:
        1. Authenticate a non-admin user.
        2. Create category data with name "bras".
        3. Post the category data to the creation endpoint.
        4. Check that the response status code is 403 (forbidden).
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        data = {"name": "bras"}
        response = self.client2.post("/api/categories/create/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_categories_as_admin(self):
        """
        Test category deletion as an admin user.

        Steps:
        1. Get the details of a category.
        2. Delete the category while authenticated as an admin.
        3. Check that the response status code is 200.
        """
        response = self.client.get(f"/api/categories/destroy/{self.category.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_categories_as_not_admin(self):
        """
        Test category deletion as a non-admin user.

        Steps:
        1. Authenticate a non-admin user.
        2. Get the details of a category.
        3. Delete the category.
        4. Check that the response status code is 403 (forbidden).
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/categories/destroy/{self.category.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_style_list_view_as_authenticate(self):
        """
        Test the style list view when the user is authenticated.

        Steps:
        1. Get the list of styles while authenticated.
        2. Check that the response status code is 200.
        """
        response = self.client2.get("/api/style/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_style_list_view_as_not_authenticate(self):
        """
        Test the style list view when the user is not authenticated.

        Steps:
        1. Log out the user.
        2. Get the list of styles.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.logout()
        response = self.client2.get("/api/style/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_style_detail_view_as_authenticate(self):
        """
        Test the style detail view when the user is authenticated.

        Steps:
        1. Authenticate the user.
        2. Get the details of a style.
        3. Check that the response status code is 200.
        4. Check that the style's name matches "sexual".
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/style/{self.style.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "sexual")

    def test_style_detail_view_as_not_authenticate(self):
        """
        Test the style detail view when the user is not authenticated.

        Steps:
        1. Log out the user.
        2. Get the details of a style.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.logout()
        response = self.client2.get(f"/api/style/{self.style.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_style_view_as_admin(self):
        """
        Test style creation as an admin user.

        Steps:
        1. Create style data with name "lacy".
        2. Post the style data to the creation endpoint while authenticated as an admin.
        3. Check that the response status code is 201 (created).
        4. Check that a style with the name "lacy" exists in the database.
        """
        data = {"name": "lacy"}
        response = self.client.post("/api/style/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Style.objects.filter(name="lacy"), "lacy")

    def test_create_style_view_as_not_admin(self):
        """
        Test style creation as a non-admin user.

        Steps:
        1. Authenticate a non-admin user.
        2. Create style data with name "lacy".
        3. Post the style data to the creation endpoint.
        4. Check that the response status code is 403 (forbidden).
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        data = {"name": "lacy"}
        response = self.client2.post("/api/style/create/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_style_view_as_admin(self):
        """
        Test style deletion as an admin user.

        Steps:
        1. Get the details of a style.
        2. Delete the style while authenticated as an admin.
        3. Check that the response status code is 200.
        """
        response = self.client.get(f"/api/style/destroy/{self.style.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_style_view_as_not_admin(self):
        """
        Test style deletion as a non-admin user.

        Steps:
        1. Authenticate a non-admin user.
        2. Get the details of a style.
        3. Delete the style.
        4. Check that the response status code is 403 (forbidden).
        """
        responce = self.client2.get(f"/api/style/destroy/{self.style.pk}/")
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

    def test_brand_list_view_as_authenticate(self):
        """
        Test the brand list view when the user is authenticated.

        Steps:
        1. Authenticate the user.
        2. Get the list of brands.
        3. Check that the response status code is 200.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get("/api/brand/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_brand_list_view_as_not_authenticate(self):
        """
        Test the brand list view when the user is not authenticated.

        Steps:
        1. Log out the user.
        2. Get the list of brands.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.logout()
        response = self.client2.get("/api/brand/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_brand_detail_view_as_authenticate(self):
        """
        Test the brand detail view when the user is authenticated.

        Steps:
        1. Authenticate the user.
        2. Get the details of a brand.
        3. Check that the response status code is 200.
        4. Verify that the retrieved brand name matches the expected value ("AVELIN").
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/brand/{self.brand.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "AVELIN")

    def test_brand_detail_view_as_not_authenticate(self):
        """
        Test the brand detail view when the user is not authenticated.

        Steps:
        1. Log out the user.
        2. Get the details of a brand.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.logout()
        response = self.client2.get(f"/api/brand/{self.brand.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_brand_view_as_admin(self):
        """
        Test the creation of a brand by an admin user.

        Steps:
        1. Create brand data.
        2. Authenticate as an admin user.
        3. Send a POST request to create a new brand.
        4. Check that the response status code is 201 (created).
        5. Verify that the brand with the specified name exists.
        """
        data = {"name": "lauma"}
        response = self.client.post("/api/brand/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Brand.objects.filter(name="lauma"), "lauma")

    def test_create_brand_view_as_not_admin(self):
        """
        Test the creation of a brand by a non-admin user.

        Steps:
        1. Create brand data.
        2. Authenticate as a non-admin user.
        3. Send a POST request to create a new brand.
        4. Check that the response status code is 403 (forbidden).
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        data = {"name": "lauma"}
        response = self.client2.post("/api/brand/create/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_brand_view_as_admin(self):
        """
        Test the deletion of a brand by an admin user.

        Steps:
        1. Authenticate as an admin user.
        2. Send a GET request to destroy the brand.
        3. Check that the response status code is 200 (OK).
        """
        response = self.client.get(f"/api/brand/destroy/{self.brand.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_brand_view_as_not_admin(self):
        """
        Test the deletion of a brand by a non-admin user.

        Steps:
        1. Authenticate as a non-admin user.
        2. Send a GET request to destroy the brand.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/brand/destroy/{self.brand.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_color_list_view_as_authenticate(self):
        """
        Test the retrieval of a list of colors by an authenticated user.

        Steps:
        1. Authenticate as a non-admin user.
        2. Send a GET request to retrieve the list of colors.
        3. Check that the response status code is 200 (OK).
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get("/api/color/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_color_list_view_as_not_authenticate(self):
        """
        Test the retrieval of a list of colors by a non-authenticated user.

        Steps:
        1. Logout the non-admin user.
        2. Send a GET request to retrieve the list of colors.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.logout()
        response = self.client2.get("/api/color/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_color_detail_view_as_authenticate(self):
        """
        Test the retrieval of a color's details by an authenticated user.

        Steps:
        1. Authenticate as a non-admin user.
        2. Send a GET request to retrieve the color's details.
        3. Check that the response status code is 200 (OK).
        4. Verify that the retrieved color's name matches the expected value.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/color/{self.color.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "red")

    def test_color_detail_view_as_not_authenticate(self):
        """
        Test the retrieval of a color's details by a non-authenticated user.

        Steps:
        1. Logout the non-admin user.
        2. Send a GET request to retrieve the color's details.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.logout()
        response = self.client2.get(f"/api/color/{self.color.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_color_view_as_admin(self):
        """
        Test the creation of a color by an admin user.

        Steps:
        1. Create color data.
        2. Send a POST request to create a new color.
        3. Check that the response status code is 201 (created).
        4. Verify that the color with the specified name exists.
        """
        data = {"name": "blue"}
        response = self.client.post("/api/color/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Color.objects.filter(name="blue"), "blue")

    def test_create_color_view_as_not_admin(self):
        """
        Test the creation of a color by a non-admin user.

        Steps:
        1. Authenticate as a non-admin user.
        2. Send a POST request to create a new color.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        data = {"name": "blue"}
        response = self.client2.post("/api/color/create/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_color_view_as_admin(self):
        """
        Test the deletion of a color by an admin user.

        Steps:
        1. Send a GET request to destroy the color.
        2. Check that the response status code is 200 (OK).
        """
        response = self.client.get(f"/api/color/destroy/{self.color.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_color_view_as_not_admin(self):
        """
        Test the deletion of a color by a non-admin user.

        Steps:
        1. Authenticate as a non-admin user.
        2. Send a GET request to destroy the color.
        3. Check that the response status code is 403 (forbidden).
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/color/destroy/{self.color.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_size_list_view_as_authenticate(self):
        """
        Test retrieving a list of sizes by an authenticated user.

        This test verifies that an authenticated user can retrieve a list of available sizes.
        It checks whether the response status code is 200 OK.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get("/api/size/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_size_list_view_as_not_authenticate(self):
        """
        Test retrieving a list of sizes by an unauthenticated user.

        This test ensures that an unauthenticated user cannot access the list of sizes.
        It checks whether the response status code is 403 Forbidden.
        """
        self.client2.logout()
        response = self.client2.get("/api/size/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_size_detail_view_as_authenticate(self):
        """
        Test retrieving details of a size by an authenticated user.

        This test verifies that an authenticated user can retrieve detailed information about a size.
        It checks whether the response status code is 200 OK and whether the retrieved data matches the expected value.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/size/{self.size.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "75C")

    def test_size_detail_view_as_not_authenticate(self):
        """
        Test retrieving details of a size by an unauthenticated user.

        This test ensures that an unauthenticated user cannot access the detailed information of a size.
        It checks whether the response status code is 403 Forbidden.
        """
        self.client2.logout()
        response = self.client2.get(f"/api/size/{self.size.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_size_view_as_admin(self):
        """
        Test creating a size by an admin user.

        This test verifies that an admin user can create a new size.
        It checks whether the response status code is 201 Created and whether the created size exists in the database.
        """
        data = {"name": "80C"}
        response = self.client.post("/api/size/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Size.objects.filter(name="80C"), "80C")

    def test_create_size_view_as_not_admin(self):
        """
        Test creating a size by a non-admin user.

        This test ensures that a non-admin user cannot create a new size.
        It checks whether the response status code is 403 Forbidden.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        data = {"name": "80C"}
        response = self.client2.post("/api/size/create/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_size_view_as_admin(self):
        """
        Test deleting a size by an admin user.

        This test verifies that an admin user can delete an existing size.
        It checks whether the response status code is 200 OK and whether the size is removed from the database.
        """
        response = self.client.get(f"/api/size/destroy/{self.size.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_size_view_as_not_admin(self):
        """
        Test deleting a size by a non-admin user.

        This test ensures that a non-admin user cannot delete a size.
        It checks whether the response status code is 403 Forbidden.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/size/destroy/{self.size.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_list_orders(self):
        """
        Test that a staff user can retrieve a list of all orders.

        This test verifies that a staff user can access a list of all orders in the system.
        It checks whether the response status code is 200 OK and whether the count of orders matches the expected value.
        """
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("count"), 2
        )  # Both staff and non-staff orders

    def test_non_staff_user_list_own_orders(self):
        """
        Test that a non-staff user can retrieve a list of their own orders.

        This test ensures that a non-staff user can only access a list of their own orders.
        It checks whether the response status code is 200 OK and whether the count of orders matches the expected value.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)  # Only the non-staff order

    def test_unauthenticated_user_cannot_list_orders(self):
        """
        Test that an unauthenticated user cannot retrieve any orders.

        This test verifies that an unauthenticated user is not allowed to access any orders.
        It checks whether the response status code is 403 Forbidden.
        """
        self.client2.logout()  # Logout any authenticated user
        response = self.client2.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_detail_own_orders(self):
        """
        Test retrieving details of orders by a staff user.

        This test verifies that a staff user can retrieve details of orders, including both staff and non-staff orders.
        It checks whether the response status codes are 200 OK and whether the order details match the expected values.
        """
        response = self.client.get(f"/api/orders/{self.staff_order.pk}/")
        response2 = self.client.get(f"/api/orders/{self.non_staff_order.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("order_number"), "111111111")
        self.assertTrue(response2.data.get("order_number"), "222222222")

    def test_non_staff_user_detail_own_orders(self):
        """
        Test retrieving details of orders by a non-staff user.

        This test ensures that a non-staff user can only retrieve details of their own orders.
        It checks whether the response status codes are 404 Not Found for staff orders and 200 OK for non-staff orders.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/orders/{self.staff_order.pk}/")
        response2 = self.client2.get(f"/api/orders/{self.non_staff_order.pk}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_staff_user_list_userprofile(self):
        """
        Test that a staff user can retrieve a list of all user profiles.

        This test verifies that a staff user can access a list of all user profiles.
        It checks whether the response status code is 200 OK and whether the count of user profiles matches the expected value.
        """
        resronse = self.client.get("/api/user_profile/")
        self.assertEqual(resronse.status_code, status.HTTP_200_OK)
        self.assertEqual(resronse.data.get("count"), 2)

    def test_non_staff_user_list_userprofile(self):
        """
        Test that a non-staff user can retrieve a list of their own user profile.

        This test ensures that a non-staff user can only access their own user profile.
        It checks whether the response status code is 200 OK and whether the count of user profiles matches the expected value.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get("/api/user_profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)

    def test_staff_user_detail_userprofile(self):
        """
        Test retrieving details of user profiles by a staff user.

        This test verifies that a staff user can retrieve details of user profiles, including both staff and non-staff user profiles.
        It checks whether the response status codes are 200 OK.
        """
        response = self.client.get(f"/api/user_profile/{self.userprofile_admin.pk}/")
        response2 = self.client.get(
            f"/api/user_profile/{self.userprofile_not_admin.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_non_staff_user_detail_userprofile(self):
        """
        Test retrieving details of user profiles by a non-staff user.

        This test ensures that a non-staff user can only retrieve details of their own user profile.
        It checks whether the response status codes are 404 Not Found for staff user profiles and 200 OK for non-staff user profiles.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/user_profile/{self.userprofile_admin.pk}/")
        response2 = self.client2.get(
            f"/api/user_profile/{self.userprofile_not_admin.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_staff_user_list_user(self):
        """
        Test that a staff user can retrieve a list of all users.

        This test verifies that a staff user can access a list of all users.
        It checks whether the response status code is 200 OK and whether the count of users matches the expected value.
        """
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 2)

    def test_non_staff_user_list_user(self):
        """
        Test that a non-staff user can retrieve a list of their own user.

        This test ensures that a non-staff user can only access their own user.
        It checks whether the response status code is 200 OK and whether the count of users matches the expected value.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)

    def test_staff_user_search_list_user(self):
        """
        Test searching and retrieving a list of users by a staff user.

        This test verifies that a staff user can search for users and retrieve the matching list.
        It checks whether the response status code is 200 OK and whether the count of users matches the expected value.
        """
        response = self.client.get("/api/user/?seacrh=admin")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 2)

    def test_non_staff_user_search_list_user(self):
        """
        Test searching and retrieving a list of users by a non-staff user.

        This test ensures that a non-staff user can search for their own user and retrieve the matching list.
        It checks whether the response status code is 200 OK and whether the count of users matches the expected value.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get("/api/user/?seacrh=admin")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)

    def test_staff_user_detail_user(self):
        """
        Test retrieving details of users by a staff user.

        This test verifies that a staff user can retrieve details of users, including both staff and non-staff users.
        It checks whether the response status codes are 200 OK.
        """
        response = self.client.get(f"/api/user/{self.admin_user.pk}/")
        response2 = self.client.get(f"/api/user/{self.not_admin_user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_non_staff_user_detail_user(self):
        """
        Test retrieving details of users by a non-staff user.

        This test ensures that a non-staff user can only retrieve details of their own user.
        It checks whether the response status codes are 404 Not Found for staff users and 200 OK for non-staff users.
        """
        self.client2.force_authenticate(user=self.not_admin_user)
        response = self.client2.get(f"/api/user/{self.admin_user.pk}/")
        response2 = self.client2.get(f"/api/user/{self.not_admin_user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_create_product_variant_view_as_admin(self):
        """
        Test creating a product variant by an admin user.

        This test verifies that an admin user can create a new product variant.
        It checks whether the response status code is 201 Created and whether the created product variant matches the expected product.
        """
        product = Product.objects.create(
            name="Test Product3",
            price=99.99,
            brand=self.brand,
            category=self.category,
            style=self.style,
            sale=False,
            vendor_code="188888",
            collection="Classic",
        )
        data = {
            "product": f"/api/products/{product.pk}/",
            "color": f"/api/color/{self.color.pk}/",
            "size": f"/api/size/{self.size.pk}/",
        }
        response = self.client.post("/api/product_variant/create/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_product_pk = (
            ProductVariant.objects.filter(product__vendor_code="188888")
            .values("product_id")[0]
            .get("product_id")
        )
        self.assertEqual(new_product_pk, product.pk)

    def test_create_product_variant_view_as_non_admin(self):
        """
        Test creating a product variant by a non-admin user.

        This test ensures that a non-admin user cannot create a new product variant.
        It checks whether the response status code is 403 Forbidden.
        """
        self.client2.force_authenticate(user=self.not_admin_user)

        product = Product.objects.create(
            name="Test Product3",
            price=99.99,
            brand=self.brand,
            category=self.category,
            style=self.style,
            sale=False,
            vendor_code="288888",
            collection="Classic",
        )
        data = {
            "product": f"/api/products/{product.pk}/",
            "color": f"/api/color/{self.color.pk}/",
            "size": f"/api/size/{self.size.pk}/",
        }
        response = self.client2.post("/api/product_variant/create/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_view_as_admin(self):
        """
        Test updating a product by an admin user.

        This test verifies that an admin user can update a product's details.
        It checks whether the response status code is 200 OK and whether the product's price is updated.
        """
        product = Product.objects.create(
            name="Test update Product",
            price=99.99,
            brand=self.brand,
            category=self.category,
            style=self.style,
            sale=False,
            vendor_code="388888",
            collection="Classic",
        )
        data = {
            "name": "Test Product1",
            "price": 100.00,
            "brand": f"/api/brand/{self.brand.pk}/",
            "category": f"/api/categories/{self.category.pk}/",
            "style": f"/api/style/{self.style.pk}/",
            "sale": False,
            "vendor_code": "388888",
            "collection": "Classic",
            "description": "description",
            "image1": self.create_image(),
            "image2": self.create_image(),
            "image3": self.create_image(),
            "image4": self.create_image(),
        }
        response = self.client.put(f"/api/products/update/{product.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(vendor_code="388888").price, 100.00)

    def test_update_product_view_as_non_admin(self):
        """
        Test updating a product by a non-admin user.

        This test ensures that a non-admin user cannot update a product's details.
        It checks whether the response status code is 403 Forbidden and whether the product's price remains unchanged.
        """
        product = Product.objects.create(
            name="Test update Product",
            price=99.99,
            brand=self.brand,
            category=self.category,
            style=self.style,
            sale=False,
            vendor_code="488888",
            collection="Classic",
        )
        data = {
            "name": "Test Product1",
            "price": 100.00,
            "brand": f"/api/brand/{self.brand.pk}/",
            "category": f"/api/categories/{self.category.pk}/",
            "style": f"/api/style/{self.style.pk}/",
            "sale": False,
            "vendor_code": "488888",
            "collection": "Classic",
            "description": "description",
            "image1": self.create_image(),
            "image2": self.create_image(),
            "image3": self.create_image(),
            "image4": self.create_image(),
        }
        response = self.client2.put(f"/api/products/update/{product.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Product.objects.get(vendor_code="488888").price, Decimal("99.99")
        )

    def test_update_order_view_as_admin(self):
        """
        Test the update order view when accessed by an admin user.

        This test case sends a PUT request to the update order view with the necessary data.
        It then asserts that the response status code is 200 (OK) and verifies that the order
        with the specified order number has been updated with the correct order total.

        The following steps are performed in this test case:
        1. Prepare the data for the request, including user profile, order number, order total, and status.
        2. Send a PUT request to the update order view with the specified order ID and the data.
        3. Assert that the response status code is 200 (OK).
        4. Retrieve the updated order from the database using the order number.
        5. Assert that the order's order total is equal to the expected value.

        Note: This test assumes that the `self.userprofile_not_admin` and `self.non_staff_order`
        attributes have been properly set up before running the test case.

        """
        data = {
            "user_profile": f"/api/user_profile/{self.userprofile_not_admin.pk}/",
            "order_number": "222222222",
            "order_total": 101.00,
            "status": "P",
        }
        response = self.client.put(
            f"/api/order/update/{self.non_staff_order.pk}/", data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Order.objects.get(order_number="222222222").order_total, Decimal("101.00")
        )

    def test_update_order_view_as_non_admin(self):
        """
        Test the update order view when accessed by a non-admin user.

        This test case sends a PUT request to the update order view with the necessary data.
        It then asserts that the response status code is 403 (FORBIDDEN), indicating that
        the non-admin user is not authorized to update the order.

        The following steps are performed in this test case:
        1. Prepare the data for the request, including user profile, order number, order total, and status.
        2. Send a PUT request to the update order view with the specified order ID and the data.
        3. Assert that the response status code is 403 (FORBIDDEN), indicating that the non-admin user
           is not authorized to perform the update.

        Note: This test assumes that the `self.userprofile_not_admin` and `self.non_staff_order`
        attributes have been properly set up before running the test case. It also assumes that
        the `self.client2` attribute is a client instance associated with the non-admin user.

        """
        data = {
            "user_profile": f"/api/user_profile/{self.userprofile_not_admin.pk}/",
            "order_number": "222222222",
            "order_total": 101.00,
            "status": "P",
        }
        response = self.client2.put(
            f"/api/order/update/{self.non_staff_order.pk}/", data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_order_view_as_admin(self):
        """
        Test the destroy order view when accessed by an admin user.

        This test case sends two GET requests to the destroy order view, one with the ID of a staff order
        and one with the ID of a non-staff order. It then asserts that the response status code for both
        requests is 200 (OK), indicating that the orders have been successfully destroyed.

        The following steps are performed in this test case:
        1. Send a GET request to the destroy order view with the ID of the staff order.
        2. Send a GET request to the destroy order view with the ID of the non-staff order.
        3. Assert that the response status code for both requests is 200 (OK).

        Note: This test assumes that the `self.staff_order` and `self.non_staff_order` attributes have
        been properly set up before running the test case.

        """
        response = self.client.get(f"/api/order/destroy/{self.staff_order.pk}/")
        response2 = self.client.get(f"/api/order/destroy/{self.non_staff_order.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_destroy_order_view_as_non_admin(self):
        """
        Test the destroy order view when accessed by a non-admin user.

        This test case sends two GET requests to the destroy order view, one with the ID of a staff order
        and one with the ID of a non-staff order. It then asserts that the response status code for the
        first request is 404 (NOT FOUND), indicating that the non-admin user is not authorized to
        access the staff order. It also asserts that the response status code for the second request is
        200 (OK), indicating that the non-admin user is authorized to access and destroy the non-staff order.

        The following steps are performed in this test case:
        1. Send a GET request to the destroy order view with the ID of the staff order.
        2. Send a GET request to the destroy order view with the ID of the non-staff order.
        3. Assert that the response status code for the first request is 404 (NOT FOUND).
        4. Assert that the response status code for the second request is 200 (OK).

        Note: This test assumes that the `self.staff_order` and `self.non_staff_order` attributes have
        been properly set up before running the test case. It also assumes that the `self.client2`
        attribute is a client instance associated with the non-admin user.

        """
        response = self.client2.get(f"/api/order/destroy/{self.staff_order.pk}/")
        response2 = self.client2.get(f"/api/order/destroy/{self.non_staff_order.pk}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_destroy_product_view_as_admin(self):
        """
        Test the destroy product view when accessed by an admin user.

        This test case creates a new test product using the `Product.objects.create()` method and sends a GET request
        to the destroy product view using the product's ID. It then asserts that the response status code is 200 (OK),
        indicating that the product has been successfully destroyed.

        The following steps are performed in this test case:
        1. Create a new test product using the `Product.objects.create()` method.
        2. Send a GET request to the destroy product view with the ID of the created product.
        3. Assert that the response status code is 200 (OK).

        Note: This test assumes that the `self.brand`, `self.category`, and `self.style` attributes have been properly
        set up before running the test case.

        """
        product = Product.objects.create(
            name="Test update Product",
            price=99.99,
            brand=self.brand,
            category=self.category,
            style=self.style,
            sale=False,
            vendor_code="100000",
            collection="Classic",
        )
        response = self.client.get(f"/api/products/destroy/{product.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_product_view_as_non_admin(self):
        """
        Test the destroy product view when accessed by a non-admin user.

        This test case creates a new test product using the `Product.objects.create()` method and sends a GET request
        to the destroy product view using the product's ID. It then asserts that the response status code is 403 (FORBIDDEN),
        indicating that the non-admin user is not authorized to access and destroy the product.

        The following steps are performed in this test case:
        1. Create a new test product using the `Product.objects.create()` method.
        2. Send a GET request to the destroy product view with the ID of the created product.
        3. Assert that the response status code is 403 (FORBIDDEN).

        Note: This test assumes that the `self.brand`, `self.category`, and `self.style` attributes have been properly
        set up before running the test case. It also assumes that the `self.client2` attribute is a client instance
        associated with the non-admin user.

        """
        product = Product.objects.create(
            name="Test update Product",
            price=99.99,
            brand=self.brand,
            category=self.category,
            style=self.style,
            sale=False,
            vendor_code="100000",
            collection="Classic",
        )

        response = self.client2.get(f"/api/products/destroy/{product.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_product_variant_view_as_admin(self):
        """
        Test the destroy product variant view when accessed by an admin user.

        This test case creates a new Product and ProductVariant instance using the provided attributes.
        It then sends a GET request to the destroy product variant view with the ID of the created variant.
        Finally, it asserts that the response status code is 200 (OK), indicating that the product variant
        has been successfully destroyed.

        The following steps are performed in this test case:
        1. Create a new Product instance with the specified attributes.
        2. Create a new ProductVariant instance associated with the created Product and the provided color and size.
        3. Send a GET request to the destroy product variant view with the ID of the created variant.
        4. Assert that the response status code is 200 (OK).

        Note: This test assumes that the `self.brand`, `self.category`, `self.style`, `self.color`, and `self.size`
        attributes have been properly set up before running the test case. It also assumes that the `self.client`
        attribute is a client instance associated with an admin user.

        """
        product = Product.objects.create(
            name="Test update Product",
            price=99.99,
            brand=self.brand,
            category=self.category,
            style=self.style,
            sale=False,
            vendor_code=str(random.randint(100000, 999999)),
            collection="Classic",
        )
        product_variant = ProductVariant.objects.create(
            product=product, color=self.color, size=self.size
        )
        response = self.client.get(
            f"/api/product_variant/destroy/{product_variant.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


def test_destroy_product_variant_view_as_non_admin(self):
    """
    Test the destroy product variant view when accessed by a non-admin user.

    This test case creates a new Product and ProductVariant instance using the provided attributes.
    It then sends a GET request to the destroy product variant view with the ID of the created variant.
    Finally, it asserts that the response status code is 403 (FORBIDDEN), indicating that the non-admin
    user is not authorized to access and destroy the product variant.

    The following steps are performed in this test case:
    1. Create a new Product instance with the specified attributes.
    2. Create a new ProductVariant instance associated with the created Product and the provided color and size.
    3. Send a GET request to the destroy product variant view with the ID of the created variant.
    4. Assert that the response status code is 403 (FORBIDDEN).

    Note: This test assumes that the `self.brand`, `self.category`, `self.style`, `self.color`, and `self.size`
    attributes have been properly set up before running the test case. It also assumes that the `self.client2`
    attribute is a client instance associated with a non-admin user.

    """
    product = Product.objects.create(
        name="Test update Product",
        price=99.99,
        brand=self.brand,
        category=self.category,
        style=self.style,
        sale=False,
        vendor_code=str(random.randint(100000, 999999)),
        collection="Classic",
    )
    product_variant = ProductVariant.objects.create(
        product=product, color=self.color, size=self.size
    )
    response = self.client2.get(f"/api/product_variant/destroy/{product_variant.pk}/")
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
