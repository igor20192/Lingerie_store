from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from paypal.standard.ipn.signals import valid_ipn_received


class WomanshopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "womanshop"

    def ready(self) -> None:
        from . import signals

        post_save.connect(signals.create_user_profile)
        valid_ipn_received.connect(signals.show_me_the_money)
        post_delete.connect(signals.update_stock_on_order_delete)
