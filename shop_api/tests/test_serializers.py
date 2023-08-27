import json
from django.urls import reverse
from io import BytesIO
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.test import APIClient, APIRequestFactory
from shop_api.serializers import UserSerializer, UserProfileSerializer
from womanshop.models import UserProfile


class UserSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "testpassword",
        }

        self.user = User.objects.create(**self.user_data)
        url = reverse("user-detail", args=[self.user.id])
        request = self.factory.get(url)
        self.serializer = UserSerializer(
            context={"request": request}, instance=self.user
        )

        self.userprofile_data = {
            "user": self.user,
            "address": "Via Callicratide 9",
            "city": "La Saxe",
            "state": "Aosta",
            "zip_code": "11013",
            "phone_number": "0337 6083509",
            "gender": "F",
        }
        self.userprofile = UserProfile.objects.create(**self.userprofile_data)
        url_userprofile = reverse("userprofile-detail", args=[self.user.id])
        request_userprofile = self.factory.get(url_userprofile)
        self.userprofile_serializer = UserProfileSerializer(
            context={"request": request_userprofile}, instance=self.userprofile
        )

    def test_user_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "is_superuser",
                    "password",
                    "groups",
                    "is_active",
                    "user_permissions",
                    "url",
                    "last_login",
                    "date_joined",
                    "is_staff",
                ]
            ),
        )

    def test_user_serializer_data_matches_user_data(self):
        data = self.serializer.data
        self.assertEqual(data["username"], self.user_data["username"])
        self.assertEqual(data["first_name"], self.user_data["first_name"])
        self.assertEqual(data["last_name"], self.user_data["last_name"])
        self.assertEqual(data["email"], self.user_data["email"])

    def test_user_serializer_json_rendering(self):
        serialized_data = json.loads(json.dumps(self.serializer.data))

        expected_data = {
            "url": f"http://testserver/api/user/{self.user.pk}/",
            "password": "testpassword",
            "last_login": None,
            "is_superuser": False,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": serialized_data["date_joined"],
            "groups": [],
            "user_permissions": [],
        }

        self.assertEqual(serialized_data, expected_data)

    def test_user_serializer_json_parsing(self):
        expected_data = {
            "url": f"http://testserver/api/user/{self.user.pk}/",
            "password": "newtestpassword",
            "last_login": None,
            "is_superuser": False,
            "username": "newtestuser",
            "first_name": "NewTest",
            "last_name": "NewUser",
            "email": "newtest@example.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2023-08-27T15:24:47.008580Z",
        }

        json_data = json.dumps(expected_data)
        stream = BytesIO(json_data.encode("utf-8"))
        parsed_data = JSONParser().parse(stream)
        serializer = UserSerializer(data=parsed_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "newtestuser")
        self.assertEqual(user.first_name, "NewTest")
        self.assertEqual(user.last_name, "NewUser")
        self.assertEqual(user.email, "newtest@example.com")

    def test_userprofile_serializer_contains_expected_fields(self):
        data = self.userprofile_serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "url",
                    "user",
                    "address",
                    "city",
                    "state",
                    "zip_code",
                    "phone_number",
                    "date_of_birth",
                    "gender",
                    "profile_pic",
                ]
            ),
        )

    def test_userprofile_serializer_data_matches_user_data(self):
        data = self.userprofile_serializer.data
        self.assertEqual(data["address"], self.userprofile_data["address"])
        self.assertEqual(data["city"], self.userprofile_data["city"])
        self.assertEqual(data["state"], self.userprofile_data["state"])
        self.assertEqual(data["zip_code"], self.userprofile_data["zip_code"])
        self.assertEqual(data["phone_number"], self.userprofile_data["phone_number"])
        self.assertEqual(data["gender"], self.userprofile_data["gender"])
