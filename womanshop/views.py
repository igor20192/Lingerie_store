from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from .models import UserProfile, Product, Style, Category, Brand
from .forms import UserProfileForm, CategoryForm, PriceForm, StyleForm, BrandForm


# Create your views here.


class UserProfileView(View):
    """Класс-представление для отображения профиля пользователя.

    Методы:
    --------
    get(self, request):
        Обработчик GET-запроса. Получает профиль пользователя по его user_id,
        создает словарь с данными контекста и отображает шаблон страницы профиля.

    Атрибуты класса:
    ------------------
    Нет атрибутов класса.

    Аргументы метода get():
    ------------------------
    request: HttpRequest
        Объект HttpRequest, содержащий данные запроса.

    Возвращает:
    -----------
    HttpResponse
        Ответ, содержащий отображение шаблона страницы профиля пользователя.

    Исключения:
    -----------
    Http404
        Если профиль пользователя не найден в базе данных.

    Пример использования:
    ---------------------
    # urls.py
    from django.urls import path
    from .views import UserProfileView

    urlpatterns = [
        path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    ]
    """

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        context = {"user_profile": user_profile}
        return render(request, "womanshop/user_profile.html", context)


class UserProfileFormView(View):
    """
    Класс представления формы редактирования профиля пользователя.

    HTTP-методы:
        - GET: выводит форму для редактирования профиля пользователя.
        - POST: сохраняет измененные данные профиля пользователя.

    Рендерит шаблон:
        - womanshop/user_profile_form.html

    Контекст:
        - form: объект формы UserProfileForm.
    """

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


def catalog_api(request):
    page_number = request.GET.get("page")
    products = Product.objects.all().order_by("price")
    paginator = Paginator(products, 3)
    page_obj = paginator.get_page(page_number)
    data = {
        "has_next": page_obj.has_next(),
        "data": [
            {
                "name": product.name,
                "price": product.price,
                "brand": product.brand.name,
                "image1": product.image1.url,
            }
            for product in page_obj.object_list
        ],
    }
    return JsonResponse(data)


class CatalogView(TemplateView):
    template_name = "womanshop/catalog.html"
    form_category = CategoryForm()
    form_price = PriceForm()
    form_style = StyleForm()
    form_brand = BrandForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_category"] = self.form_category
        context["form_price"] = self.form_price
        context["form_style"] = self.form_style
        context["form_brand"] = self.form_brand

        # Получаем номер текущей страницы, переданной GET-параметром
        page_number = self.request.GET.get("page")
        products = Product.objects.all().order_by("price")
        paginator = Paginator(
            products, 3
        )  # Определяем пагинатор с количеством товаров на странице равным 12
        page_obj = paginator.get_page(
            page_number
        )  # Получаем страницу с номером page_number

        context[
            "list_product"
        ] = page_obj  # Передаем объект страницы в контекст шаблона
        context["catalog_api_url"] = reverse("catalog_api")

        return context

    def post(self, request, *args, **kwargs):
        form_category = CategoryForm(request.POST)
        form_style = StyleForm(request.POST)
        form_brand = BrandForm(request.POST)
        form_price = PriceForm(request.POST)
        if form_category.is_valid():
            categories = [k for k, v in form_category.cleaned_data.items() if v]
        if form_style.is_valid():
            styles = [k for k, v in form_style.cleaned_data.items() if v]
        if form_brand.is_valid():
            brands = [k.upper() for k, v in form_brand.cleaned_data.items() if v]
        if form_price.is_valid():
            start_price = form_price.cleaned_data.get("start")
            end_price = form_price.cleaned_data.get("end")
        filters = Q()
        if categories:
            filters &= Q(category__name__in=categories)
        if styles:
            filters &= Q(style__name__in=styles)
        if brands:
            filters &= Q(brand__name__in=brands)
        if start_price:
            filters &= Q(price__gt=start_price)
        if end_price:
            filters &= Q(price__lt=end_price)

        context = self.get_context_data()

        # Фильтруем продукты и создаем объект страницы с количеством товаров на странице равным 12
        products = Product.objects.filter(filters).order_by("price")
        paginator = Paginator(products, 3)
        page_obj = paginator.get_page(1)

        context[
            "list_product"
        ] = page_obj  # Передаем объект страницы в контекст шаблона

        return self.render_to_response(context)
