from decimal import Decimal
import json
from typing import Any, Dict
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from .models import UserProfile, Product, Size, ProductVariant, Color, Category
from .forms import UserProfileForm


# Create your views here.

LOGIN_URL = "/accounts/signup/"


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


def product_api(request):
    """
    API view for retrieving product data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing product data.

    Raises:
        Http404: If the specified category does not exist.
    """

    # Get the request parameters
    page_number = request.GET.get("page")  # Page number
    category = request.GET.get("category_by")  # Product category
    product_id = request.GET.get("product_id")  # Product ID

    # Get the category ID based on the category name
    category_id = get_object_or_404(Category, name=category).id

    # Filter products by category and exclude the specified product
    products = Product.objects.filter(category_id=category_id).exclude(
        id=int(product_id)
    )

    # Create a paginator to split the products into pages
    paginator = Paginator(products, 3)

    # Get the page object based on the page number
    page_obj = paginator.get_page(page_number)

    # Create a dictionary with product data
    data = {
        "has_next": page_obj.has_next(),  # Flag indicating if there is a next page
        "data": [
            {
                "name": product.name,  # Product name
                "price": product.price,  # Product price
                "brand": product.brand.name,  # Product brand
                "image1": product.image1.url,  # URL of the first product image
                "id": product.id,  # Product ID
            }
            for product in page_obj.object_list  # Iterate over objects on the current page
        ],
    }

    return JsonResponse(data)  # Return a JSON response with the data


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
        context["favorites_id"] = json.dumps(self.request.session.get("favorite", []))

        return context


class ProductDetailView(TemplateView):
    """View class for displaying product details."""

    template_name = "womanshop/product.html"

    def get_context_data(self, **kwargs):
        """Get the context data for rendering the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data.

        """
        context = super().get_context_data(**kwargs)
        product_id = kwargs.get("product_id")
        product = Product.objects.get(
            id=product_id
        )  # Get the product object based on the id
        product_variant = ProductVariant.objects.filter(
            product_id=product.id
        )  # Get the product variants
        colors = {
            obj.color.name for obj in product_variant
        }  # Get unique colors from the product variants
        data = []
        user = self.request.user

        # Check if the product is in favorites and add the favorite flag to the context if it is
        if product_id in self.request.session.get("favorite", []):
            context["favorite"] = True

        for color in list(colors):
            # Create a dictionary with information about the color and associated sizes
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

        context["product"] = product  # Add the product object to the context
        context["data"] = data  # Add the list of data to the context
        context[
            "user"
        ] = (
            user.is_authenticated
        )  # Add information about the authenticated user to the context
        context[
            "product_variant"
        ] = product_variant  # Add the product variants to the context
        context["item_in_cart"] = len(
            self.request.session.get("cart", [])
        )  # Add the count of items in the cart to the context
        context["favorites_id"] = json.dumps(self.request.session.get("favorite", []))

        return context  # Return the context data


class AddToCartView(LoginRequiredMixin, View):
    """
    View class to add a product to the cart for authenticated users.
    """

    login_url = LOGIN_URL  # Замените это на ваш URL для страницы регистрации или входа

    def post(self, request, product_id):
        """
        Handle POST request to add a product to the cart.

        Args:
            request: The HTTP request object.
            product_id: The ID of the product to add to the cart.

        Returns:
            A JSON response indicating the success or failure of the operation.
        """
        data = request.body.decode("utf-8")  # Get data from the request
        if data:
            # Parse data from JSON
            json_data = json.loads(data)
            color = json_data.get("color")
            size = json_data.get("size")
            quantity = json_data.get("quantity")

            if color and size and quantity:
                cart = request.session.get("cart", [])
                cart.append([product_id, color, size, quantity])
                request.session["cart"] = cart
                # Fetch stock information from the database
                product = get_object_or_404(Product, id=product_id)
                color_id = get_object_or_404(Color, name=color).id
                size_id = get_object_or_404(Size, name=size).id
                stock = ProductVariant.objects.filter(
                    product=product, color_id=color_id, size_id=size_id
                ).values("stock")
                # Return a successful response
                return JsonResponse(
                    {
                        "message": "Data received and processed successfully.",
                        "stock": stock[0]["stock"],
                    }
                )

        # If no data was provided or the request method is not POST, return an error
        return JsonResponse(
            {"message": "Error: No data provided or request method is not POST."},
            status=400,
        )


class AvailableProductQuantityView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        """
        Get the available quantity of a product variant based on color and size.

        Args:
            request (HttpRequest): The HTTP request object.
            product_id (int): The ID of the product.

        Returns:
            JsonResponse: JSON response containing the available stock quantity.
        """
        data = request.body.decode("utf-8")
        if data:
            # Parse data from JSON
            json_data = json.loads(data)
            color = json_data.get("color")
            size = json_data.get("size")

            if color and size:
                product = get_object_or_404(Product, id=product_id)
                color_id = get_object_or_404(Color, name=color).id
                size_id = get_object_or_404(Size, name=size).id
                stock = ProductVariant.objects.filter(
                    product=product, color_id=color_id, size_id=size_id
                ).values("stock")

                # Return JSON response with stock quantity
                return JsonResponse({"stock": stock[0]["stock"]})


class CartView(LoginRequiredMixin, TemplateView):
    login_url = LOGIN_URL
    template_name = "womanshop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get("cart", [])
        product_data = []
        for id, data in enumerate(cart):
            product_obj = get_object_or_404(Product, id=data[0])
            color = get_object_or_404(Color, name=data[1])
            size = get_object_or_404(Size, name=data[2])
            stock = ProductVariant.objects.filter(
                product=product_obj, color_id=color.id, size_id=size.id
            ).values("stock")
            subtotal = product_obj.price * Decimal(data[3])
            product_data.append(
                {
                    "id": id,
                    "product": product_obj,
                    "quantity": data[3],
                    "subtotal": subtotal,
                    "stock": stock[0]["stock"],
                    "color": color.name,
                    "size": size.name,
                }
            )
        item_id = [[item["id"], item["stock"]] for item in product_data]
        context["items_id"] = json.dumps(item_id)
        context["cart_items"] = product_data
        context["cart_total"] = sum(item["subtotal"] for item in product_data)
        context["item_in_cart"] = len(self.request.session.get("cart", []))
        return context


class RemoveFromCartView(LoginRequiredMixin, View):
    """
    View class for removing an item from the cart.
    The user must be authenticated, otherwise will be redirected to the signup page.
    """

    login_url = LOGIN_URL

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
    """
    View class to clear the cart.
    """

    login_url = LOGIN_URL

    def get(self, request):
        """
        Handle GET request to clear the cart.

        Args:
            request: The HTTP request object.

        Returns:
            A redirect to the "cart" URL.
        """
        if request.session.get("cart"):
            request.session["cart"] = []
            return redirect("cart")


class CartQuantityUpdateView(LoginRequiredMixin, View):
    """
    View class for updating the quantity of items in the cart.

    Attributes:
        login_url (str): The URL for the login page.

    Methods:
        post(self, request): Handles the POST request for updating the quantity of items in the cart.

    """

    login_url = LOGIN_URL

    def post(self, request):
        """
        Handle the POST request for updating the quantity of items in the cart.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating the status of the update.

        """
        data = request.body.decode("utf-8")
        cart = request.session.get("cart")

        if data and cart:
            json_data = json.loads(data)
            quantity = json_data.get("quantity")
            index = json_data.get("index")
            cart[index][3] = quantity
            request.session["cart"] = cart
            return JsonResponse({"message": "Количество товаров в корзине обновлено."})

        return JsonResponse(
            {"message": "Error: No data provided or request method is not POST."},
            status=400,
        )


class AddFavorite(View):
    """View class for adding a product to favorites."""

    def post(self, request):
        """Handles the POST request for adding a product to favorites.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            JsonResponse: The JSON response.

        """
        data = request.body.decode("utf-8")
        favorite = request.session.get("favorite", [])
        if data:
            json_data = json.loads(data)
            favorite_id = json_data.get("favorite")
            favorite.append(int(favorite_id))
            request.session["favorite"] = list(set(favorite))
            return JsonResponse({"message": "Товар добавлен в фавориты."})
        return JsonResponse(
            {"message": "Error: No data provided or request method is not POST."},
            status=400,
        )


class RemoveFromFavorites(View):
    """View class for removing a product from favorites."""

    def post(self, request):
        """Handles the POST request for removing a product from favorites.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            JsonResponse: The JSON response.

        """
        data = request.body.decode("utf-8")
        if request.session.get("favorite") and data:
            favorites = request.session["favorite"]
            json_data = json.loads(data)
            favorite_id = json_data.get("favorite")

            if int(favorite_id) in favorites:
                favorites.remove(int(favorite_id))
                request.session["favorite"] = favorites
                return JsonResponse({"message": "Product removed from favorites."})
            return JsonResponse(
                {"message": "Error: Not a favorite or request method is not POST."},
                status=400,
            )
        return JsonResponse(
            {"message": "Error: No data provided or request method is not POST."},
            status=400,
        )
