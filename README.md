# Lingerie store Online Store

An online store project based on Django.

## Models

### UserProfile

The UserProfile model contains user profile information, including address, phone number, and date of birth.

### Order

The Order model represents information about orders. It includes the order number, order date, total cost and order status.

### Category, Style, Brand, Color, Size

The Category, Style, Brand, Color, and Size models provide information about product categories, styles, brands, colors, and sizes, respectively.

### Product

The Product model contains product data such as title, category, price, and images.

### ProductVariant

The ProductVariant model associates products with their characteristics, such as color and size.

### OrderItem

The OrderItem model represents the individual items in an order. It contains information about the product, quantity, price and subtotal.


## Installation

To use the project, follow these steps:

1. Clone the repository: `https://github.com/igor20192/Lingerie_store.git`
2. Go to directory: `cd Lingerie_store`
3. Create a Python virtual environment: `python3 -m venv venv`
4. Activate Python virtual environment: `. venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Set up project settings, including database settings and secret key.

## Usage

1. Apply database migrations: `python manage.py migrate`
2. Run local server: `python manage.py runserver`
3. Open a browser and navigate to `http://localhost:8000`

## Views

The project contains the following views:

### IndexView

Main page of the store. Shows popular products, promotions and new items.

### UserProfileView

View user profile. The user can view their details such as address, phone number and date of birth. *(Authorization required)*.

### UserProfileFormView

User profile editing form. Allows the user to update information about themselves, such as address and phone number. *(Authorization required)*.

### CatalogView

Products catalog. Displays all available products divided into categories.

### ProductDetailView

Detailed product page. Shows detailed information about the selected product, its images and characteristics.

### AddToCartView

Adding an item to the cart. Allows the user to add a product to the shopping cart.

### cartview

Shopping basket. Displays all items added to the cart, their quantity and total cost.

### RemoveFromCartView

Removing an item from the cart. Allows the user to remove an item from the cart.

### ClearCartView

Emptying the basket. Allows the user to completely empty the trash.

### AvailableProductQuantityView

View the available quantity of the item. Returns the number of available items for the selected product.

### CartQuantityUpdateView

Update the quantity of items in the cart. Allows the user to update the quantity of an item in the cart.

### AddFavorite

Adding a product to favorites. Allows the user to add a product to the favorites list.

### RemoveFromFavorites

Removing a product from favorites. Allows the user to remove a product from the favorites list.

### CheckoutTemplateView

Checkout page. Shows information about the order and provides an option for payment.

### PayPalPaymentView

Payment processing via PayPal. Allows the user to make a payment using PayPal.

### PayPalSuccessView

Order successful completion page. Shows information about the completed order after a successful payment via PayPal.

### search_view

Search for goods. Allows the user to search for products by keyword.

## URLs (URLs)

Example URLs for accessing views:

- Main page: `/`
- User profile: `/user_profile/`
- Profile editing: `/user_profile_form/`
- Product catalog: `/catalog/`
- Product detail page: `/product/<int:product_id>/`
- Adding a product to the cart: `/add_to_cart/<int:product_id>/`
- Shopping cart: `/cart/`
- Removing an item from the cart: `/remove_from_cart/<int:id>/`
- Empty cart: `/clear_cart/`
- and others...

## Signals

The project uses signals to handle various events:

- `create_user_profile`: Create a user profile when creating a new user.
- `show_me_the_money`: Handling successful PayPal payments.
- `update_stock_on_order_delete`: Update stock on order deletion.

## Code examples

### Here are some examples of URL routes to access different views of your online store:

```python
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # ... Other URL routes ...

    # View Access URL Examples
    path('user_profile/', login_required(views.UserProfileView.as_view()), name='user_profile'),
    path('add_to_cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/<str:cart_total>/', views.CheckoutTemplateView.as_view(), name='checkout'),
    path('paypal_payment/', views.PayPalPaymentView.as_view(), name='paypal_payment'),
    path('success/<str:order_number>/<str:order_total>/', views.PayPalSuccessView.as_view(), name='success'),
    path('payment_canceled/', TemplateView.as_view(template_name='paypal/payment_canceled.html'), name='payment_canceled'),
    path('search/', views.search_view, name='search'),
]
```

### An example of using the UserProfileView view:

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from .models import UserProfile

@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    model = UserProfile
    template_name = 'user_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.userprofile
```

### An example of using the AddToCartView view:

```python
from django.shortcuts import redirect
from django.views import View
from .models import Product, Cart

class AddToCartView(View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.add_product(product)
        return redirect('cart')
```

### An example of using the PayPalPaymentView:

```python
from django.views.generic import View
from django.shortcuts import redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

class PayPalPaymentView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': cart.total(),
            'item_name': 'Order #{}'.format(cart.id),
            'invoice': str(cart.id),
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('success')),
            'cancel_return': request.build_absolute_uri(reverse('payment_canceled')),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'paypal_payment.html', {'form': form})
```

### An example of using the search_view view to search for products:

```python
from django.shortcuts import render
from django.db.models import Q
from .models import Product

def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'search_results.html', {'products': products})
```
## API Endpoints

### Products
- `GET /api/products/`: List all products.
- `GET /api/products/<int:pk>/`: Retrieve a product instance.
- `POST /api/products/create/`: Create a new product (Admin only).
- `PUT /api/products/update/<int:pk>/`: Update a product instance (Admin only).
- `DELETE /api/products/destroy/<int:pk>/`: Delete a product instance (Admin only).

### Categories
- `GET /api/categories/`: List all categories.
- `GET /api/categories/<int:pk>/`: Retrieve a category instance.
- `POST /api/categories/create/`: Create a new category (Admin only).
- `DELETE /api/categories/destroy/<int:pk>/`: Delete a category instance (Admin only).

### Orders
- `GET /api/orders/`: List all orders (Authenticated users and Admins).
- `GET /api/orders/<int:pk>/`: Retrieve an order instance (Authenticated users and Admins).
- `PUT /api/order/update/<int:pk>/`: Update an order instance (Authenticated users and Admins).
- `DELETE /api/order/destroy/<int:pk>/`: Delete an order instance (Authenticated users and Admins).

### Styles, Brands, Colors, Sizes
- Endpoints for listing, retrieving, creating, and deleting individual instances of styles, brands, colors, and sizes follow a similar pattern as above.

### Product Variants
- Endpoints for listing, retrieving, creating, updating, and deleting product variants follow a similar pattern as above.

### User Profiles
- Endpoints for listing and retrieving user profiles are available for Admins only.

### Users
- Endpoints for listing and retrieving users are available for Admins only.

Please note that some endpoints require authentication or Admin permissions.

## Shop API

### Views

Here are the views available in the Shop API:

#### Products

- `GET /api/products/`: List all products.
- `GET /api/products/<int:pk>/`: Retrieve a product instance.
- `POST /api/products/create/`: Create a new product instance (Admin only).
- `PUT /api/products/update/<int:pk>/`: Update a product instance (Admin only).
- `DELETE /api/products/destroy/<int:pk>/`: Delete a product instance (Admin only).

#### Categories

- `GET /api/categories/`: List all categories.
- `GET /api/categories/<int:pk>/`: Retrieve a category instance.
- `POST /api/categories/create/`: Create a new category instance (Admin only).
- `DELETE /api/categories/destroy/<int:pk>/`: Delete a category instance (Admin only).

#### Orders

- `GET /api/orders/`: List orders (Authenticated users and Admins).
- `GET /api/orders/<int:pk>/`: Retrieve an order instance (Authenticated users and Admins).
- `PUT /api/order/update/<int:pk>/`: Update an order instance (Authenticated users and Admins).
- `DELETE /api/order/destroy/<int:pk>/`: Delete an order instance (Authenticated users and Admins).

#### Styles

- `GET /api/style/`: List all styles.
- `GET /api/style/<int:pk>/`: Retrieve a style instance.
- `POST /api/style/create/`: Create a new style instance (Admin only).
- `DELETE /api/style/destroy/<int:pk>/`: Delete a style instance (Admin only).

#### Brands

- `GET /api/brand/`: List all brands.
- `GET /api/brand/<int:pk>/`: Retrieve a brand instance.
- `POST /api/brand/create/`: Create a new brand instance (Admin only).
- `DELETE /api/brand/destroy/<int:pk>/`: Delete a brand instance (Admin only).

#### Colors

- `GET /api/color/`: List all colors.
- `GET /api/color/<int:pk>/`: Retrieve a color instance.
- `POST /api/color/create/`: Create a new color instance (Admin only).
- `DELETE /api/color/destroy/<int:pk>/`: Delete a color instance (Admin only).

#### Sizes

- `GET /api/size/`: List all sizes.
- `GET /api/size/<int:pk>/`: Retrieve a size instance.
- `POST /api/size/create/`: Create a new size instance (Admin only).
- `DELETE /api/size/destroy/<int:pk>/`: Delete a size instance (Admin only).

### Permissions

- `IsAuthenticated`: Accessible to authenticated users.
- `IsAdminUser`: Accessible to admin users.

Please note that certain actions require appropriate permissions. See each view's documentation for details.


## Authors

The project is developed and maintained by Igor Udovenko.

## Contributing

Contributions are welcome! If you have any bug fixes, improvements, or new features, please submit a pull request.
## License

This project is licensed under the MIT License - see the LICENSE file for details.
