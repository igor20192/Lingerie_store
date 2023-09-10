from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
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
