from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, date
from ..models import UserProfile, Order


class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Создаем объект UserProfile, связанный с тестовым пользователем
        cls.user_profile = UserProfile.objects.create(
            user=cls.user,
            address="123 Main St",
            city="Test City",
            state="CA",
            zip_code="12345",
            phone_number="555-1234",
            date_of_birth=date(1990, 1, 1),
            gender="M",
            profile_pic=None,
        )

    def test_userprofile_model(self):
        # Проверяем, что созданный объект UserProfile корректно сохраняет поля
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.address, "123 Main St")
        self.assertEqual(self.user_profile.city, "Test City")
        self.assertEqual(self.user_profile.state, "CA")
        self.assertEqual(self.user_profile.zip_code, "12345")
        self.assertEqual(self.user_profile.phone_number, "555-1234")
        self.assertEqual(self.user_profile.date_of_birth, date(1990, 1, 1))
        self.assertEqual(self.user_profile.gender, "M")
        self.assertIsNone(self.user_profile.profile_pic.name)

        # Проверяем, что __str__() метод возвращает правильное значение
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_order_model(self):
        # Создаем объект Order
        order = Order.objects.create(
            user_profile=self.user_profile,
            order_number="1234567890",
            order_date=datetime.now(),
            order_total=100.00,
            status="P",
        )

        # Проверяем, что созданный объект Order корректно сохраняет поля
        self.assertEqual(order.user_profile, self.user_profile)
        self.assertEqual(order.order_number, "1234567890")
        self.assertIsNotNone(order.order_date)
        self.assertEqual(order.order_total, 100.00)
        self.assertEqual(order.status, "P")

        # Проверяем, что __str__() метод возвращает правильное значение
        self.assertEqual(str(order), "1234567890")
