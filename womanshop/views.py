from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import UserProfile
from .forms import UserProfileForm


# Create your views here.


class UserProfileView(View):
    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        context = {"user_profile": user_profile}
        return render(request, "womanshop/user_profile.html", context)


class UserProfileFormView(View):
    def get(self, request):
        # Получение экземпляра модели UserProfile для текущего пользователя
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        # Создание экземпляра формы с дефолтными значениями из модели
        form = UserProfileForm(instance=user_profile)

        return render(request, "womanshop/user_profile_form.html", {"form": form})

    def post(self, request):
        # Логика для POST-запроса
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            # Дополнительная логика после успешного сохранения формы
            return redirect("user_profile")  # Перенаправление на страницу профиля

            # Обработка ошибок формы
        return render(request, "womanshop/user_profile_form.html", {"form": form})
