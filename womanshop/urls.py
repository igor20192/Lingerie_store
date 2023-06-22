from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "user_profile/",
        login_required(views.UserProfileView.as_view()),
        name="user_profile",
    ),
    path(
        "user_profile_form/",
        views.UserProfileFormView.as_view(),
        name="user_profile_form",
    ),
    path("catalog/", views.CatalogView.as_view(), name="catalog"),
    path("catalog_api/", views.catalog_api, name="catalog_api"),
    path(
        "product/<int:product_id>/",
        views.ProductDetailView.as_view(),
        name="product",
    ),
    path(
        "add_to_cart/<int:product_id>/",
        views.AddToCartView.as_view(),
        name="add_to_cart",
    ),
    path("cart/", views.CartView.as_view(), name="cart"),
    path(
        "remove_from_cart/<int:id>/",
        views.RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path("clear_cart/", views.ClearCartView.as_view(), name="clear_cart"),
    path(
        "available_product_quantity/<int:product_id>/",
        views.AvailableProductQuantityView.as_view(),
        name="available_product_quantity",
    ),
]
