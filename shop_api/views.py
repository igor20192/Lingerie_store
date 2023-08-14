from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from womanshop.models import (
    Product,
    Order,
    Category,
    Style,
    Brand,
    UserProfile,
    ProductVariant,
    Color,
    Size,
)
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    StyleSerializer,
    BrandSerializer,
    UserProfileSerializer,
    UserSerializer,
    ProductVariantSerializer,
    ColorSerializer,
    SizeSerializer,
)
from django.contrib.auth.models import User


class ProductListAPIView(generics.ListAPIView):
    """
    List all products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a product instance.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"


class ProductVariantListAPIView(generics.ListAPIView):
    """
    List all product variants.
    """

    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()


class ProductVriantDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a product variant instance.
    """

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = "pk"


class CategoryListAPIView(generics.ListAPIView):
    """
    List all categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a category instance.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "pk"


class CategoryCreateAPIView(generics.CreateAPIView):
    """
    Create a new category instance (accessible to admin users).

    This view allows admin users to create a new category instance.

    - To create a category, make a POST request to the endpoint with required data.

    Permissions:
    - Admin users have permission to create new categories.

    Request data format (for POST request):
    {
        "name": "Category Name",
        ...
    }

    Response format (for successful POST request):
    HTTP 201 Created
    {
        "id": 10,
        "name": "Category Name",
        ...
    }
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class CategoryDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a category instance (accessible to admin users).

    This view allows retrieving and deleting a category instance by its primary key (ID).
    Admin users have full access to retrieve and delete any category instance.

    - To retrieve a category, make a GET request to the endpoint for a specific category.
    - To delete a category, make a DELETE request to the endpoint for a specific category.

    Permissions:
    - Admin users have full access (read and delete) to all categories.

    URL example:
    GET /api/categories/3/ - Retrieve details of category with ID 3.
    DELETE /api/categories/3/ - Delete category with ID 3.

    Response format (for GET request):
    {
        "id": 3,
        "name": "Category Name",
        ...
    }

    Response format (for DELETE request):
    HTTP 204 No Content
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class StyleListAPIView(generics.ListAPIView):
    """
    List all styles.
    """

    queryset = Style.objects.all()
    serializer_class = StyleSerializer


class StyleDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a style instance.
    """

    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    lookup_field = "pk"


class StyleCreateAPIView(generics.CreateAPIView):
    """
    Create a new style instance (accessible to admin users).

    This view allows admin users to create a new style instance.

    - To create a style, make a POST request to the endpoint with required data.

    Permissions:
    - Admin users have permission to create new styles.

    Request data format (for POST request):
    {
        "name": "Style Name",
        ...
    }

    Response format (for successful POST request):
    HTTP 201 Created
    {
        "id": 10,
        "name": "Style Name",
        ...
    }
    """

    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    permission_classes = [IsAdminUser]


class StyleDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a style instance (accessible to admin users).

    This view allows retrieving and deleting a style instance by its primary key (ID).
    Admin users have full access to retrieve and delete any style instance.

    - To retrieve a style, make a GET request to the endpoint for a specific style.
    - To delete a style, make a DELETE request to the endpoint for a specific style.

    Permissions:
    - Admin users have full access (read and delete) to all styles.

    URL example:
    GET /api/styles/3/ - Retrieve details of style with ID 3.
    DELETE /api/styles/3/ - Delete style with ID 3.

    Response format (for GET request):
    {
        "id": 3,
        "name": "Style Name",
        ...
    }

    Response format (for DELETE request):
    HTTP 204 No Content
    """

    queryset = Style.objects.all()
    serializer_class = StyleSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class BrandListAPIView(generics.ListAPIView):
    """
    List all brands.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a brand instance.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "pk"


class BrandCreateAPIView(generics.CreateAPIView):
    """
    Create a new brand instance (accessible to admin users).

    This view allows admin users to create a new brand instance.

    - To create a brand, make a POST request to the endpoint with required data.

    Permissions:
    - Admin users have permission to create new brands.

    Request data format (for POST request):
    {
        "name": "Brand Name",
        ...
    }

    Response format (for successful POST request):
    HTTP 201 Created
    {
        "id": 10,
        "name": "Brand Name",
        ...
    }
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]


class BrandDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a brand instance (accessible to admin users).

    This view allows retrieving and deleting a brand instance by its primary key (ID).
    Admin users have full access to retrieve and delete any brand instance.

    - To retrieve a brand, make a GET request to the endpoint for a specific brand.
    - To delete a brand, make a DELETE request to the endpoint for a specific brand.

    Permissions:
    - Admin users have full access (read and delete) to all brands.

    URL example:
    GET /api/brands/3/ - Retrieve details of brand with ID 3.
    DELETE /api/brands/3/ - Delete brand with ID 3.

    Response format (for GET request):
    {
        "id": 3,
        "name": "Brand Name",
        ...
    }

    Response format (for DELETE request):
    HTTP 204 No Content
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class ColorListAPIView(generics.ListAPIView):
    """
    List all colors.
    """

    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ColorDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a color instance.
    """

    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    lookup_field = "pk"


class ColorCreateAPIView(generics.CreateAPIView):
    """
    Create a new color instance (accessible to admin users).

    This view allows admin users to create a new color instance.

    - To create a color, make a POST request to the endpoint with required data.

    Permissions:
    - Admin users have permission to create new colors.

    Request data format (for POST request):
    {
        "name": "Color Name",
        ...
    }

    Response format (for successful POST request):
    HTTP 201 Created
    {
        "id": 10,
        "name": "Color Name",
        ...
    }
    """

    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser]


class ColorDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a color instance (accessible to admin users).

    This view allows retrieving and deleting a color instance by its primary key (ID).
    Admin users have full access to retrieve and delete any color instance.

    - To retrieve a color, make a GET request to the endpoint for a specific color.
    - To delete a color, make a DELETE request to the endpoint for a specific color.

    Permissions:
    - Admin users have full access (read and delete) to all colors.

    URL example:
    GET /api/colors/3/ - Retrieve details of color with ID 3.
    DELETE /api/colors/3/ - Delete color with ID 3.

    Response format (for GET request):
    {
        "id": 3,
        "name": "Color Name",
        ...
    }

    Response format (for DELETE request):
    HTTP 204 No Content
    """

    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class SizeListAPIView(generics.ListAPIView):
    """
    List all sizes.
    """

    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class SizeDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a size instance.
    """

    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    lookup_field = "pk"


class SizeCreateAPIView(generics.CreateAPIView):
    """
    Create a new size instance (accessible to admin users).

    This view allows admin users to create a new size instance.

    - To create a size, make a POST request to the endpoint with required data.

    Permissions:
    - Admin users have permission to create new sizes.

    Request data format (for POST request):
    {
        "name": "Size Name",
        ...
    }

    Response format (for successful POST request):
    HTTP 201 Created
    {
        "id": 10,
        "name": "Size Name",
        ...
    }
    """

    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser]


class SizeDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a size instance (accessible to admin users).

    This view allows retrieving and deleting a size instance by its primary key (ID).
    Admin users have full access to retrieve and delete any size instance.

    - To retrieve a size, make a GET request to the endpoint for a specific size.
    - To delete a size, make a DELETE request to the endpoint for a specific size.

    Permissions:
    - Admin users have full access (read and delete) to all sizes.

    URL example:
    GET /api/sizes/3/ - Retrieve details of size with ID 3.
    DELETE /api/sizes/3/ - Delete size with ID 3.

    Response format (for GET request):
    {
        "id": 3,
        "name": "Size Name",
        ...
    }

    Response format (for DELETE request):
    HTTP 204 No Content
    """

    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class OrderListAPIView(generics.ListAPIView):
    """
    List orders (accessible to authenticated users and staff).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user_profile=self.request.user.userprofile)


class OrderDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve an order instance (accessible to authenticated users and staff).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user_profile=self.request.user.userprofile)


class UserProfileListView(generics.ListAPIView):
    """
    List user profiles (accessible to admin users).
    """

    permission_classes = [IsAdminUser]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.all()


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a user profile instance (accessible to admin users).
    """

    permission_classes = [IsAdminUser]
    serializer_class = UserProfileSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return UserProfile.objects.all()


class UserListAPIView(generics.ListAPIView):
    """
    List users (accessible to admin users).
    """

    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve a user instance (accessible to admin users).
    """

    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return User.objects.all()


class ProductCreateAPIView(generics.CreateAPIView):
    """
    Create a new product instance (accessible to admin users).
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductVariantCreateAPIViews(generics.CreateAPIView):
    """
    Create a new product variant instance (accessible to admin users).
    """

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUser]


class ProductUpdateAPIViews(generics.UpdateAPIView):
    """
    Update a product instance (accessible to admin users).
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductVariantUpdateAPIViews(generics.UpdateAPIView):
    """
    Update a product variant instance (accessible to admin users).
    """

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAdminUser]


class OrderUpdateAPIView(generics.UpdateAPIView):
    """
    Update an order instance (accessible to authenticated users and staff).
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user_profile=self.request.user.userprofile)


class OrderDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete an order instance (accessible to authenticated users).

    This view allows retrieving and deleting an order instance. If the user is an admin,
    all orders are accessible for retrieval and deletion. For regular authenticated users,
    they can only retrieve and delete their own orders.

    - To retrieve an order, make a GET request to the endpoint for a specific order.
    - To delete an order, make a DELETE request to the endpoint for a specific order.

    Permissions:
    - Admin users have full access (read and delete) to all orders.
    - Authenticated users can retrieve and delete their own orders.

    URL example:
    GET /api/orders/3/ - Retrieve details of order with ID 3.
    DELETE /api/orders/3/ - Delete order with ID 3.

    Request headers:
    - Authorization: Token <user-token> (for authenticated users)

    Response format (for GET request):
    {
        "id": 3,
        "user_profile": 2,
        "status": "Pending",
        ...
    }

    Response format (for DELETE request):
    HTTP 204 No Content
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user_profile=self.request.user.userprofile)


class ProductDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a product instance (accessible to admin users).

    This view allows retrieving and deleting a product instance by its primary key (ID).
    Admin users have full access to retrieve and delete any product instance.

    - To retrieve a product, make a GET request to the endpoint for a specific product.
    - To delete a product, make a DELETE request to the endpoint for a specific product.

    Permissions:
    - Admin users have full access (read and delete) to all products.

    URL example:
    GET /api/products/5/ - Retrieve details of product with ID 5.
    DELETE /api/products/5/ - Delete product with ID 5.

    Response format (for GET request):
    {
        "id": 5,
        "name": "Product Name",
        "price": 49.99,
        ...
    }

    Response format (for DELETE request):
    HTTP 204 No Content
    """

    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    lookup_field = "pk"


class ProductVariantDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a product variant instance (accessible to admin users).

    This view allows retrieving and deleting a product variant instance by its primary key (ID).
    Admin users have full access to retrieve and delete any product variant instance.

    - To retrieve a product variant, make a GET request to the endpoint for a specific product variant.
    - To delete a product variant, make a DELETE request to the endpoint for a specific product variant.

    Permissions:
    - Admin users have full access (read and delete) to all product variants.

    URL example:
    GET /api/product_variants/8/ - Retrieve details of product variant with ID 8.
    DELETE /api/product_variants/8/ - Delete product variant with ID 8.

    Response format (for GET request):
    {
        "id": 8,
        "product": 5,
        "color": "Red",
        ...
    }

    Response format (for DELETE request):
    HTTP 204 No Content
    """

    queryset = ProductVariant.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ProductVariantSerializer
    lookup_field = "pk"