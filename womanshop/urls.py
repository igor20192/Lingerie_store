from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="womanshop/index.html"), name="index"),
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
]
