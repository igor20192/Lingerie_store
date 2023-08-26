from decimal import Decimal
from datetime import datetime
import json
from typing import Any, Dict
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from .models import (
    UserProfile,
    Product,
    Size,
    ProductVariant,
    Color,
    Category,
    Order,
    OrderItem,
)
from .forms import UserProfileForm


# Create your views here.

LOGIN_URL = "/accounts/signup/"

# Constants for filtering
CATEGORS = {
    "bodysuit",
    "bras",
    "tights_and_socks",
    "swimwear",
    "men_underwear",
    "panties",
    "seamless_underwear",
    "thermal_underwear",
    "accessories",
}
STYLES = {
    "basic_underwear",
    "new_style",
    "сomfort_underwear",
    "sexual",
    "lacy",
    "everyday",
    "homewear",
    "sleepwear",
    "for_wedding",
}
BRANDS = {
    "AVELIN",
    "COMAZO",
    "LAUMA",
    "MELADO",
    "MILAVITSA",
    "SERGE",
    "TEATRO",
    "TRIUMPH",
}
SIZE = {"80B", "80C", "80D", "80E", "80F"}


class IndexView(TemplateView):
    """
    View for displaying the index/home page.

    Attributes:
        template_name (str): The name of the template used for rendering the index page.

    Methods:
        get_context_data(**kwargs): Retrieves context data for rendering the index page.

    """

    template_name = "womanshop/index.html"

    def get_context_data(self, **kwargs):
        """
        Retrieves context data for rendering the index page.

        Returns:
            dict: A dictionary containing the context data for the template.

        """

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


def filter_data(request, data):
    """
    Filter data based on the request.

    Args:
        request (HttpRequest): The HTTP request object.
        data (list): The list of data to filter.

    Returns:
        list: The filtered data.

    """
    categories = request.GET.get("categors")
    return [
        value
        for value in data
        if (request.GET.get(value.lower()) == "true") or (categories == value.lower())
    ]


def filters_categors_xxl():
    """
    Retrieves the product_id values of ProductVariant objects that have a size name in the SIZE list.

    Returns:
        JsonResponse: The JSON response containing the filtered product_id values. If no matching product_id values are found, an empty JSON response is returned.
    """
    size_xxl_id = ProductVariant.objects.filter(size__name__in=SIZE).values(
        "product_id"
    )
    if not size_xxl_id:
        data = {"data": []}
        return JsonResponse(data)
    return Product.objects.filter(id__in=size_xxl_id).values("id")


def filters_categors_sale():
    """
    Retrieves the id values of Product objects that have the sale field set to True.

    Returns:
        JsonResponse: The JSON response containing the filtered id values. If no matching id values are found, an empty JSON response is returned.
    """
    product_sale = Product.objects.filter(sale=True).values("id")
    if not product_sale:
        data = {"data": []}
        return JsonResponse(data)
    return product_sale


def filters_catalog_products(
    categors, style, brand, startprice, endprice, xxl, sale, sortdirect, sortby
):
    """
    Filters and sorts the products based on the given filter parameters.

    Parameters:
        categors (list): The list of category names to filter by.
        style (list): The list of style names to filter by.
        brand (list): The list of brand names to filter by.
        startprice (int): The minimum price to filter by.
        endprice (int): The maximum price to filter by.
        xxl (set): The set of product_id values for the "XXL" category.
        sale (set): The set of id values for the "sale" category.
        sortdirect (str): The sort direction ("asc" or "desc").
        sortby (str): The field to sort by.

    Returns:
        queryset: The filtered and sorted queryset of Product objects.
    """
    filters = Q()
    if categors:
        filters &= Q(category__name__in=categors)
    if style:
        filters &= Q(style__name__in=style)
    if brand:
        filters &= Q(brand__name__in=brand)
    if startprice:
        filters &= Q(price__gt=startprice)
    if endprice:
        filters &= Q(price__lt=endprice)
    # Determine the sort direction
    if sortdirect == "desc":
        sortby = f"-{sortby}"
    # Apply additional filters based on "XXL" or "sale" category
    if xxl:
        filters &= Q(id__in=xxl)
    if sale:
        filters &= Q(id__in=sale)
    # Filter and sort the products
    return Product.objects.filter(filters).order_by(sortby)


def paginator_products(products, pg_number, number):
    """
    Paginate a list of products.

    Args:
        products (list): The list of products to paginate.
        pg_number (int): The page number to retrieve.

    Returns:
        Paginator: The paginated page object.

    """
    paginator = Paginator(products, number)
    return paginator.get_page(pg_number)


def create_response_data(pg_obj):
    """
    Create response data for a paginated object.

    Args:
        pg_obj (Paginator): The paginated object.

    Returns:
        dict: The response data.

    """
    data = {
        "has_next": pg_obj.has_next(),
        "data": [
            {
                "name": product.name,
                "price": product.price,
                "brand": product.brand.name,
                "image1": product.image1.url,
                "id": product.id,
            }
            for product in pg_obj.object_list
        ],
    }
    return data


def catalog_api(request):
    """
    API endpoint for catalog data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: The JSON response.

    """
    page_number = request.GET.get("page")
    sort_by = request.GET.get("sort_by")
    sort_direction = request.GET.get("sort_direction")
    start_price = request.GET.get("start")
    end_price = request.GET.get("end")
    categors = request.GET.get("categors")

    product_xxl = set()
    product_sale_id = set()

    # Check for specific category "XXL" or "sale" to filter the products
    if categors == "XXL":
        product_xxl = filters_categors_xxl()

    if categors == "sale":
        product_sale_id = filters_categors_sale()

    # Create the filters based on the selected categories, styles, brands, and price range
    filtered_categories = filter_data(request, CATEGORS)
    filters_style = filter_data(request, STYLES)
    filters_brand = filter_data(request, BRANDS)

    products = filters_catalog_products(
        filtered_categories,
        filters_style,
        filters_brand,
        start_price,
        end_price,
        product_xxl,
        product_sale_id,
        sort_direction,
        sort_by,
    )
    page_obj = paginator_products(products, page_number, 12)

    return JsonResponse(create_response_data(page_obj))


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

    page_obj = paginator_products(products, page_number, 3)

    return JsonResponse(
        create_response_data(page_obj)
    )  # Return a JSON response with the data


def search_view(request):
    """
    View function for handling product search.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing the search results.

    """
    search_term = request.GET.get("q")
    results = []

    if search_term:
        # Perform case-insensitive search for products that contain the search term in their name
        results = Product.objects.filter(name__icontains=search_term).values(
            "id", "name"
        )

    return JsonResponse(list(results), safe=False)


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
        categors = self.request.GET.get("categors")

        context["categors"] = categors

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
    """
    View for displaying the shopping cart page.

    Attributes:
        login_url (str): The URL to redirect to for login. Used by the LoginRequiredMixin.
        template_name (str): The name of the template used for rendering the shopping cart page.

    Methods:
        get_context_data(**kwargs): Retrieves context data for rendering the shopping cart page.

    """

    login_url = LOGIN_URL
    template_name = "womanshop/cart.html"

    def get_context_data(self, **kwargs):
        """
        Retrieves context data for rendering the shopping cart page.

        Returns:
            dict: A dictionary containing the context data for the template.

        """

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


class CheckoutTemplateView(TemplateView):
    template_name = "womanshop/order.html"

    def get_context_data(self, cart_total, **kwargs):
        """
        Override the get_context_data method to include order creation and clearing the cart.

        Args:
            cart_total (str): Total amount of the cart.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user)
        user_profile = get_object_or_404(UserProfile, user=user)
        cart_items = self.request.session.get("cart", [])
        if cart_items:
            with transaction.atomic():
                order = Order.objects.create(
                    user_profile=user_profile,
                    order_number=self.generate_order_number(),
                    order_total=self.get_cart_total(cart_items),
                    status="P",
                )

            for item in cart_items:
                color = get_object_or_404(Color, name=item[1])
                size = get_object_or_404(Size, name=item[2])
                product_variant = get_object_or_404(
                    ProductVariant,
                    product_id=item[0],
                    color_id=color.id,
                    size_id=size.id,
                )
                OrderItem.objects.create(
                    order=order,
                    product_variant=product_variant,
                    quantity=item[3],
                    price=product_variant.product.price,
                    subtotal=product_variant.product.price * Decimal(item[3]),
                )
                ProductVariant.objects.filter(id=product_variant.id).update(
                    stock=product_variant.stock - int(item[3])
                )
        self.request.session["cart"] = []
        context["order"] = order
        return context

    @staticmethod
    def generate_order_number():
        """
        Generate a unique order number based on the current timestamp.

        Returns:
            str: Generated order number.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        order_number = f"ORD-{timestamp}"
        return order_number

    @staticmethod
    def get_cart_total(cart):
        """
        Calculate the total amount of the cart.

        Args:
            cart (list): List of cart items.

        Returns:
            decimal.Decimal: Total amount of the cart.
        """
        total_cart = []
        for data in cart:
            product = get_object_or_404(Product, id=data[0])
            subtotal = product.price * Decimal(data[3])
            total_cart.append(subtotal)
        return sum(total_cart)


class PayPalSuccessView(TemplateView):
    """
    View for displaying the success page after a successful PayPal payment.

    Attributes:
        template_name (str): The name of the template used for rendering the success page.

    Methods:
        get_context_data(order_number, order_total, **kwargs): Retrieves context data for rendering the success page.

    """

    template_name = "paypal/success.html"

    def get_context_data(self, order_number, order_total, **kwargs):
        """
        Retrieves context data for rendering the success page.

        Args:
            order_number (str): The order number for the successful payment.
            order_total (str): The total amount of the order for the successful payment.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the context data for the template.

        """

        context = super().get_context_data(**kwargs)
        context["order_number"] = order_number
        context["order_total"] = order_total
        return context


class PayPalPaymentView(View):
    """
    View for processing payments through PayPal.

    Methods:
        post(request): Handles the POST request to create a payment through PayPal.
    """

    def post(self, request):
        """
        Handles the POST request to create a payment through PayPal.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            HttpResponse: The HTTP response with the template for PayPal payment.
        """

        context = dict(
            order_number=request.POST.get("order_number"),
            order_date=request.POST.get("order_date"),
            order_total=request.POST.get("order_total"),
        )

        paypal_dict = {
            "add": "1",
            "no_shipping": 2,
            "business": settings.PAYPAL_BUSINESS,
            "amount": Decimal(context["order_total"]),
            "item_name": context["order_number"],
            "invoice": request.POST.get("order_id"),
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return": request.build_absolute_uri(
                reverse(
                    "success", args=[context["order_number"], context["order_total"]]
                )
            ),
            "cancel_return": request.build_absolute_uri(reverse("payment_canceled")),
            "custom": "premium_plan",
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context["form"] = form
        return render(request, "paypal/payment.html", context)
