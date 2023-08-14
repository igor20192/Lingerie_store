from django.test import TestCase
from rest_framework.test import APIRequestFactory
from shop_api.views import ProductListAPIView, ProductDetailAPIView
from womanshop.models import Product, Brand, Category, Style
from django.shortcuts import get_object_or_404


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
        self.assertEqual(response.data["name"], "Test Product")
