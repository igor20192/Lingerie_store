from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    A form for editing a user's profile.
    """

    class Meta:
        model = UserProfile
        fields = [
            "address",
            "city",
            "state",
            "zip_code",
            "phone_number",
            "date_of_birth",
            "gender",
            "profile_pic",
        ]

        widgets = {
            "profile_pic": forms.ClearableFileInput(
                attrs={"multiple": True}
            ),  # Setting up a widget to download media files
        }
        widgets["profile_pic"].attrs.update({"enctype": "multipart/form-data"})

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Set default values for form fields from model fields
        self.initial["address"] = self.instance.address
        self.initial["city"] = self.instance.city
        self.initial["state"] = self.instance.state
        self.initial["zip_code"] = self.instance.zip_code
        self.initial["phone_number"] = self.instance.phone_number
        self.initial["date_of_birth"] = self.instance.date_of_birth
        self.initial["gender"] = self.instance.gender
