from decimal import Decimal
import json
from typing import Any, Dict
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from .models import UserProfile, Product, Size, ProductVariant, Color
from .forms import UserProfileForm


# Create your views here.


class IndexView(TemplateView):
    template_name = "womanshop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_in_cart"] = len(self.request.session.get("cart", []))
        return context


class UserProfileView(View):
    """Class-based view for displaying a user profile.

    Methods:
        get(self, request): Handles GET requests. Retrieves the user profile based on the user_id,
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
        return render(request, "womanshop/user_profile.html", context)


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

        return render(request, "womanshop/user_profile_form.html", {"form": form})

    def post(self, request):
        """
        Handle POST requests and save the modified user profile data.
        """
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect("user_profile")

        return render(request, "womanshop/user_profile_form.html", {"form": form})


def catalog_api(request):
    """
    Performs filtering and sorting of products based on the parameters provided in the request.GET.
    Returns the result in JSON format.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing the filtered and sorted products.

    """
    page_number = request.GET.get("page")
    sort_by = request.GET.get("sort_by")
    sort_direction = request.GET.get("sort_direction")
    start_price = request.GET.get("start")
    end_price = request.GET.get("end")

    # Define name lists for categories, styles, and brands
    name_categor = (
        "bodysuit",
        "bras",
        "tights_and_socks",
        "swimwear",
        "men_underwear",
        "panties",
        "seamless_underwear",
        "thermal_underwear",
        "accessories",
    )
    name_styles = (
        "basic_underwear",
        "new_style",
        "сomfort_underwear",
        "sexual",
        "lacy",
        "everyday",
        "homewear",
        "sleepwear",
        "for_wedding",
    )
    name_brands = (
        "avelin",
        "comazo",
        "lauma",
        "melado",
        "milavitsa",
        "serge",
        "teatro",
        "triumph",
    )

    # Filter categories, styles, and brands based on the request parameters
    categories = [
        values for values in name_categor if request.GET.get(values) == "true"
    ]
    styles = [values for values in name_styles if request.GET.get(values) == "true"]
    brands = [
        values.upper() for values in name_brands if request.GET.get(values) == "true"
    ]

    # Create the filters based on the selected categories, styles, brands, and price range
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

    # Determine the sort direction
    if sort_direction == "desc":
        sort_by = f"-{sort_by}"

    # Filter and sort the products
    products = Product.objects.filter(filters).order_by(sort_by)

    # Paginate the products
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)

    # Create the response data
    data = {
        "has_next": page_obj.has_next(),
        "data": [
            {
                "name": product.name,
                "price": product.price,
                "brand": product.brand.name,
                "image1": product.image1.url,
                "id": product.id,
            }
            for product in page_obj.object_list
        ],
    }

    return JsonResponse(data)


class CatalogView(TemplateView):
    """View for displaying the catalog page."""

    template_name = "womanshop/catalog.html"

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data for the catalog page.

        Returns:
            dict: The context data containing the product list, pagination information, and API URL.
        """
        context = super().get_context_data(**kwargs)

        # Get the current page number from the GET parameters
        page_number = self.request.GET.get("page")

        # Retrieve all products and order them by price
        products = Product.objects.all().order_by("price")

        # Create a paginator with 12 products per page
        paginator = Paginator(products, 12)

        # Get the page object for the specified page number
        page_obj = paginator.get_page(page_number)

        # Add the page object to the context
        context["list_product"] = page_obj

        # Add the API URL to the context using the reverse function
        context["catalog_api_url"] = reverse("catalog_api")

        # Displaying the number of items in the cart
        context["item_in_cart"] = len(self.request.session.get("cart", []))

        return context


class ProductDetailView(TemplateView):
    template_name = "womanshop/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get("product_id")
        product = Product.objects.get(id=product_id)
        product_variant = ProductVariant.objects.filter(product_id=product.id)
        colors = {obj.color.name for obj in product_variant}
        data = []
        for color in list(colors):
            data.append(
                {
                    "color": color,
                    "sizes": ",".join(
                        [
                            obj.size.name
                            for obj in product_variant
                            if color == obj.color.name
                        ]
                    ),
                }
            )
        context["product"] = product
        context["data"] = data
        context["product_variant"] = product_variant
        context["item_in_cart"] = len(self.request.session.get("cart", []))
        return context


class AddToCartView(View):
    def post(self, request, product_id):
        data = request.body.decode("utf-8")  # Получаем данные из запроса
        if data:
            # Парсим данные из JSON
            json_data = json.loads(data)
            color = json_data.get("color")
            size = json_data.get("size")
            quantity = json_data.get("quantity")

            if color and size and quantity:
                cart = self.request.session.get("cart", [])
                cart.append([product_id, color, size, quantity])
                self.request.session["cart"] = cart
                color_id = Color.objects.get(name=color).id
                size_id = Size.objects.get(name=size).id
                stock = ProductVariant.objects.filter(
                    product_id=product_id, color_id=color_id, size_id=size_id
                ).values("stock")
                # Возвращаем успешный ответ
                return JsonResponse(
                    {
                        "message": "Данные успешно получены и обработаны. ",
                        "stock": stock[0]["stock"],
                    }
                )

        # Если данные не были переданы или запрос не был методом POST,
        # возвращаем ошибку
        return JsonResponse(
            {"message": "Ошибка: данные не были переданы или запрос не является POST."},
            status=400,
        )


class CartView(LoginRequiredMixin, TemplateView):
    login_url = "/accounts/signup/"
    template_name = "womanshop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", [])
        product_data = []
        for id, data in enumerate(cart):
            product_obj = Product.objects.get(id=data[0])
            subtotal = product_obj.price * Decimal(data[3])
            product_data.append(
                {
                    "id": id,
                    "product": product_obj,
                    "quantity": data[3],
                    "subtotal": subtotal,
                }
            )

        context["cart_items"] = product_data
        context["cart_total"] = sum(item["product"].price for item in product_data)
        context["item_in_cart"] = len(self.request.session.get("cart", []))
        return context


class ClearCartView(LoginRequiredMixin, View):
    """
    View class for removing an item from the cart.
    The user must be authenticated, otherwise will be redirected to the signup page.
    """

    login_url = "/accounts/signup/"

    def get(self, request, id):
        """
        Handles the GET request for removing an item from the cart.

        Args:
            request (HttpRequest): The request object.
            id (int): The identifier of the item to remove.

        Returns:
            HttpResponseRedirect: Redirects to the cart page.
        """
        item_cart = request.session.get("cart")
        if item_cart and str(id):
            del item_cart[id]
            request.session["cart"] = item_cart
        return redirect("cart")


class ClearCartView(LoginRequiredMixin, View):
    login_url = "/accounts/signup/"

    def get(self, request):
        if request.session.get("cart"):
            request.session["cart"] = []
            return redirect("cart")
