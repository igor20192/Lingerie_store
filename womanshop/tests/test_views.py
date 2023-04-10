from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from womanshop.models import UserProfile
from womanshop.views import UserProfileFormView
from datetime import date


class UserProfileViewTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Создаем тестовый профиль пользователя
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            address="Test Address",
            city="Test City",
            state="Test State",
            zip_code="Test Zip",
            phone_number="Test Phone",
            date_of_birth=date(2000, 1, 1),
            gender="M",
        )

    def test_user_profile_view_get(self):
        # Входим в систему как тестовый пользователь
        self.client.login(username="testuser", password="testpassword")
        # Получаем URL для UserProfileView
        url = reverse("user_profile")
        # Отправляем GET-запрос
        response = self.client.get(url)
        # Проверяем, что ответ имеет код 200 (успешный ответ)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что в ответе есть ожидаемые данные из профиля пользователя
        self.assertContains(response, "Test Address")
        self.assertContains(response, "Test City")
        self.assertContains(response, "Test State")
        self.assertContains(response, "Test Zip")
        self.assertContains(response, "Test Phone")
        dod_str = str(
            response.context[1].__dict__["dicts"][3]["user_profile"].date_of_birth
        )
        self.assertEqual(dod_str, "2000-01-01")
        self.assertContains(response, "M")

    def test_user_profile_view_get_unauthenticated(self):
        # Выходим из системы (не аутентифицированное состояние)
        self.client.logout()
        # Получаем URL для UserProfileView
        url = reverse("user_profile")
        # Отправляем GET-запрос
        response = self.client.get(url)
        # Проверяем, что ответ имеет код 302 (перенаправление на страницу входа)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что пользователь был перенаправлен на страницу входа
        self.assertRedirects(
            response, "/accounts/login/?next=" + reverse("user_profile")
        )


class UserProfileFormViewTest(TestCase):
    def setUp(self):
        # Создание фабрики запросов
        self.factory = RequestFactory()

        # Создание пользователя
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Создание файла для тестирования загрузки media-файлов
        self.uploaded_file = SimpleUploadedFile(
            "profile_pic.jpg", content=b"", content_type="image/jpeg"
        )

        # Создание экземпляра модели UserProfile для пользователя
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            address="Test address",
            city="Test city",
            state="Test state",
            zip_code="zip code",
            phone_number="Test phone number",
            date_of_birth="2000-01-01",
            gender="M",
            profile_pic=self.uploaded_file,
        )

    def test_get_method(self):
        # Создание GET-запроса
        request = self.factory.get("/user_profile_form")
        request.user = self.user

        # Создание экземпляра класса UserProfileFormView
        view = UserProfileFormView.as_view()

        # Выполнение GET-запроса и получение HTTP-ответа
        response = view(request)

        # Проверка статуса HTTP-ответа
        self.assertEqual(response.status_code, 200)

        # Проверка, что форма в контексте содержит ожидаемые значения
        self.assertContains(response, "Test address")
        self.assertContains(response, "Test city")
        self.assertContains(response, "Test state")
        self.assertContains(response, "zip code")
        self.assertContains(response, "Test phone number")
        self.assertContains(response, "M")
        self.assertContains(response, "2000-01-01")
        user_profile = UserProfile.objects.get(user=self.user).profile_pic

        # Проверка вновь созданого profile_pic
        self.assertContains(response, user_profile.name)

    def test_post_method(self):
        # Создание POST-запроса
        request = self.factory.post(
            "/user_profile_form/",
            data={
                "address": "Updated address",
                "gender": "M",
                "city": "test_city",
                "state": "test_state",
                "zip_code": "61177",
                "phone_number": "0935678934",
                "date_of_birth": date(2000, 1, 1),
            },
        )
        request.user = self.user
        # Создание экземпляра класса UserProfileFormView
        view = UserProfileFormView.as_view()

        # Выполнение POST-запроса и получение HTTP-ответа
        response = view(request)
        # Проверка статуса HTTP-ответа
        self.assertEqual(response.status_code, 302)

        # Проверка, что форма была успешно сохранена
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.address, "Updated address")
