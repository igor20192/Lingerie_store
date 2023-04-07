from django.apps import AppConfig
from django.db.models.signals import post_save


class WomanshopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "womanshop"

    def ready(self) -> None:
        from . import signals

        post_save.connect(signals.create_user_profile)
