from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views


urlpatterns = [
    path("products/", views.ProductListAPIView.as_view(), name="product-list-api"),
    path(
        "products/<int:pk>/",
        views.ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    path("categories/", views.CategoryListAPIView.as_view(), name="category-list-api"),
    path(
        "categories/<int:pk>/",
        views.CategoryDetailAPIView.as_view(),
        name="category-detail",
    ),
    path("orders/", views.OrderListAPIView.as_view(), name="order-list-api"),
    path("orders/<int:pk>/", views.OrderDetailAPIView.as_view(), name="order-detail"),
    path("orders_item/", views.OrderItemListAPIView.as_view(), name="orderitem-list"),
    path(
        "orders_item/<int:pk>/",
        views.OpderItemDetailAPIView.as_view(),
        name="orderitem-detail",
    ),
    path("style/", views.StyleListAPIView.as_view(), name="style-list"),
    path("style/<int:pk>/", views.StyleDetailAPIView.as_view(), name="style-detail"),
    path("brand/", views.BrandListAPIView.as_view(), name="brand-list"),
    path("brand/<int:pk>/", views.BrandDetailAPIView.as_view(), name="brand-detail"),
    path("user_profile/", views.UserProfileListView.as_view(), name="userprofile-list"),
    path(
        "user_profile/<int:pk>/",
        views.UserProfileDetailAPIView.as_view(),
        name="userprofile-detail",
    ),
    path("user/", views.UserListAPIView.as_view(), name="user-list"),
    path("user/<int:pk>/", views.UserDetailAPIView.as_view(), name="user-detail"),
    path(
        "product_variant/",
        views.ProductVariantListAPIView.as_view(),
        name="productvariant-list",
    ),
    path(
        "product_variant/<int:pk>/",
        views.ProductVariantDetailAPIView.as_view(),
        name="productvariant-detail",
    ),
    path("color/", views.ColorListAPIView.as_view(), name="color-list"),
    path("color/<int:pk>/", views.ColorDetailAPIView.as_view(), name="color-detail"),
    path("size/", views.SizeListAPIView.as_view(), name="size-list"),
    path("size/<int:pk>/", views.SizeDetailAPIView.as_view(), name="size-detail"),
    # To create, update and delete products
    path(
        "products/create/", views.ProductCreateAPIView.as_view(), name="product-create"
    ),
    path(
        "products/update/<int:pk>/",
        views.ProductUpdateAPIViews.as_view(),
        name="product-update",
    ),
    path(
        "products/destroy/<int:pk>/",
        views.ProductDestroyAPIView.as_view(),
        name="product-destroy",
    ),
    # To create, update and delete product_variant
    path(
        "product_variant/create/",
        views.ProductVariantCreateAPIViews.as_view(),
        name="productvariant-create",
    ),
    path(
        "product_variant/update/<int:pk>/",
        views.ProductVariantUpdateAPIViews.as_view(),
        name="product-update",
    ),
    path(
        "product_variant/destroy/<int:pk>/",
        views.ProductVariantDestroyAPIView.as_view(),
        name="productvariant-destroy",
    ),
    # To update and delete order
    path(
        "order/update/<int:pk>/",
        views.OrderUpdateAPIView.as_view(),
        name="order-update",
    ),
    path(
        "order/destroy/<int:pk>/",
        views.OrderDestroyAPIView.as_view(),
        name="order-destroy",
    ),
    # To create and delete categories
    path(
        "categories/create/",
        views.CategoryCreateAPIView.as_view(),
        name="category-create",
    ),
    path(
        "categories/destroy/<int:pk>/",
        views.CategoryDestroyAPIView.as_view(),
        name="category-destroy",
    ),
    # To create and delete style
    path("style/create/", views.StyleCreateAPIView.as_view(), name="style-create"),
    path(
        "style/destroy/<int:pk>/",
        views.StyleDestroyAPIView.as_view(),
        name="style-destroy",
    ),
    # To create and delete brand
    path("brand/create/", views.BrandCreateAPIView.as_view(), name="brand-create"),
    path(
        "brand/destroy/<int:pk>/",
        views.BrandDestroyAPIView.as_view(),
        name="brand-destroy",
    ),
    # To create and delete color
    path("color/create/", views.ColorCreateAPIView.as_view(), name="color-create"),
    path(
        "color/destroy/<int:pk>/",
        views.ColorDestroyAPIView.as_view(),
        name="color-destroy",
    ),
    # To create and delete size
    path("size/create/", views.SizeCreateAPIView.as_view(), name="size-create"),
    path(
        "size/destroy/<int:pk>/",
        views.SizeDestroyAPIView.as_view(),
        name="size-destroy",
    ),
]
# Apply formatting to endpoints
urlpatterns = format_suffix_patterns(urlpatterns)
