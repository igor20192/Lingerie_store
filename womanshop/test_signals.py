from django.test import TestCase
from .models import UserProfile, User
from django.db.models.signals import post_save
from .signals import create_user_profile


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user", password="123434sad4d")

    def test_create_user_profile(self):
        # Подписываемся на сигнал сохранения объекта User
        post_save.connect(create_user_profile, sender=User)

        # Проверяем, что объект UserProfile был создан
        user_profile = UserProfile.objects.filter(user=self.user)
        self.assertTrue(user_profile.exists())

        # Проверяем, что создан правильно
        self.assertEqual(user_profile[0].user.username, "test_user")

        # Отправляем сигнал post_save повторно
        post_save.connect(create_user_profile, sender=User)

        # Проверяем, что UserProfile не создается повторно
        self.assertEqual(user_profile.count(), 1)
