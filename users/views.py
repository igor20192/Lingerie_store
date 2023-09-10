from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import UserProfile
from womanshop.forms import UserProfileForm


# Create your views here.
class UserProfileView(View):
    """Class-based view for displaying a user profile.

    Methods:
        get(self, request): Handles GET requests. Retrieves the user profile based on the user
            creates a context dictionary, and renders the profile page template.

    Class Attributes:
        None.

    Args for get() method:
        request (HttpRequest): The HttpRequest object containing the request data.

    Returns:
        HttpResponse: A response containing the rendered user profile page template.

    Raises:
        Http404: If the user profile is not found in the database.

    Example Usage:
        # urls.py
        from django.urls import path
        from .views import UserProfileView

        urlpatterns = [
            path('user_profile/', UserProfileView.as_view(), name='user_profile'),
        ]
    """

    def get(self, request):
        """Handle GET requests and render the user profile page."""
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        context = {"user_profile": user_profile}
        return render(request, "users/user_profile.html", context)


class UserProfileFormView(View):
    """
    Class-based view for editing a user profile.

    HTTP Methods:
        - GET: Displays the form for editing the user profile.
        - POST: Saves the modified user profile data.

    Renders Template:
        - womanshop/user_profile_form.html

    Context:
        - form: UserProfileForm object.

    """

    def get(self, request):
        """
        Handle GET requests and display the user profile form for editing.
        """
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        form = UserProfileForm(instance=user_profile)

        return render(request, "users/user_profile_form.html", {"form": form})

    def post(self, request):
        """
        Handle POST requests and save the modified user profile data.
        """
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect("user_profile")

        return render(request, "users/user_profile_form.html", {"form": form})
