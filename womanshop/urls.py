from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
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
    path(
        "cart_quantity_update/",
        views.CartQuantityUpdateView.as_view(),
        name="cart_quantity_update",
    ),
    path("product_api/", views.product_api, name="product_api"),
    path("add_favorite/", views.AddFavorite.as_view(), name="add_favorite"),
    path(
        "remove_from_favorites/",
        views.RemoveFromFavorites.as_view(),
        name="remove_from_favorites",
    ),
    path(
        "checkout/<str:cart_total>/",
        views.CheckoutTemplateView.as_view(),
        name="checkout",
    ),
    path(
        "paypal_payment/",
        views.PayPalPaymentView.as_view(),
        name="paypal_payment",
    ),
    path(
        "success/<str:order_number>/<str:order_total>",
        views.PayPalSuccessView.as_view(),
        name="success",
    ),
    path(
        "payment_canceled/",
        TemplateView.as_view(template_name="paypal/payment_canceled.html"),
        name="payment_canceled",
    ),
    path("search/", views.search_view, name="search"),
]
