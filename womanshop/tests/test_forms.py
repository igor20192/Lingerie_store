from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from womanshop.models import UserProfile
from womanshop.forms import UserProfileForm


class UserProfileFormTest(TestCase):
    def setUp(self):
        # Создание пользователя
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Создание файла для тестирования загрузки media-файлов
        self.uploaded_file = SimpleUploadedFile(
            "profile_pic.jpg", content=b"", content_type="image/jpeg"
        )

        # Создание экземпляра модели UserProfile для использования в тестах
        self.user_profile = UserProfile.objects.create(
            user=self.user,  # Значение поля user не используется в форме, так как оно устанавливается в представлении
            address="Test address",
            city="Test city",
            state="Test state",
            zip_code="zip code",
            phone_number="Test phone number",
            date_of_birth="2000-01-01",
            gender="M",
            profile_pic=self.uploaded_file,
        )

    def test_form_valid_data(self):
        # Создание формы с валидными данными
        form = UserProfileForm(
            data={
                "address": "Updated address",
                "city": "Updated city",
                "state": "Updated state",
                "zip_code": "Newcode",
                "phone_number": "Updated phone number",
                "date_of_birth": "2001-01-01",
                "gender": "F",
            },
            instance=self.user_profile,
        )

        # Проверка, что форма валидна
        self.assertTrue(form.is_valid())

        # Сохранение формы
        form.save()

        # Проверка, что значения в модели UserProfile обновлены
        user_profile = UserProfile.objects.get(pk=self.user_profile.pk)
        self.assertEqual(
            user_profile.address, "Updated address"
        )  # Ожидаемое значение поля address

    def test_form_invalid_data(self):
        # Создание формы с невалидными данными
        form = UserProfileForm(
            data={
                "address": "",  # Пустое значение, не проходящее валидацию
                "city": "Updated city",
                "state": "Updated state",
                "zip_code": "Newcode",
                "phone_number": "Updated phone number",
                "date_of_birth": "2001-01-01",
                "gender": "F",  # Значение, проходящее валидацию
            },
            instance=self.user_profile,
        )

        # Проверка, что форма не валидна
        self.assertFalse(form.is_valid())

        # Проверка наличия ошибок валидации в форме
        self.assertIn("address", form.errors)  # Проверка наличия ошибки в поле address

    def test_form_rendering(self):
        # Создание формы для рендеринга
        form = UserProfileForm(instance=self.user_profile)

        # Проверка наличия полей формы в HTML-ответе

        self.assertIn(
            "Test address", form.as_p()
        )  # Проверка наличия значения поля address в HTML-ответе
        self.assertIn(
            "Test city", form.as_p()
        )  # Проверка наличия значения поля city в HTML-ответе
        self.assertIn(
            "zip code", form.as_p()
        )  # Проверка наличия значения поля zip_code в HTML-ответе
        self.assertIn(
            "Test phone number", form.as_p()
        )  # Проверка наличия значения поля phone_nuber в HTML-ответе
        self.assertIn(
            "2000-01-01", form.as_p()
        )  # Проверка наличия значения поля  date_of_birth в HTML-ответе
        self.assertIn(
            "M", form.as_p()
        )  # Проверка наличия значения поля gender в HTML-ответе
        user_profile = UserProfile.objects.get(pk=self.user_profile.pk).profile_pic
        self.assertIn(
            user_profile.name, form.as_p()
        )  # Проверка наличия значения поля profile_pic в HTML-ответе
