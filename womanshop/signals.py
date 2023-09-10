from sys import argv
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Order, OrderItem, ProductVariant
from users.models import UserProfile
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.core.exceptions import ValidationError


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    """
    Signal post_save that creates a user profile when a new user is created.
    Args:
        sender: The model class that initiated the signal.
        instance: The model instance that was saved.
    Returns:
        None
    """
    if "test" not in argv:
        obj = User.objects.filter(id=instance.id)
        if not (UserProfile.objects.filter(user_id=instance.id)) and obj:
            UserProfile.objects.create(user=obj[0])


@receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    """
    Signal valid_ipn_received that handles successful PayPal payments.
    Args:
        sender: The class that initiated the signal.
        **kwargs: Additional arguments.
    Returns:
        None
    """
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_BUSINESS:
            # Not a valid payment
            return
        order = get_object_or_404(Order, pk=ipn_obj.invoice)
        if (
            ipn_obj.mc_gross == round(Decimal(order.order_total))
            and ipn_obj.mc_currency == "USD"
        ):
            order.status = "O"
            order.save()
        else:
            raise ValueError("Paypal ipn_obj data not valid!")


@receiver(post_delete, sender=Order)
def update_stock_on_order_delete(sender, instance, **kwargs):
    """
    Signal post_delete that updates the product stock when an order is deleted.
    Args:
        sender: The model class that initiated the signal.
        instance: The model instance that was deleted.
    Returns:
        None
    """
    if isinstance(instance, OrderItem):
        product_variant = get_object_or_404(
            ProductVariant, id=instance.product_variant_id
        )
        product_variant.stock += instance.quantity
        product_variant.save()
        order = get_object_or_404(Order, id=instance.order_id)
        order.order_total -= instance.subtotal
        order.save()
