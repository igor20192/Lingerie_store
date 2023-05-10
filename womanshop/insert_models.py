import random
from datetime import datetime
from .models import Product, Category, Style, Brand, Color, Size


# Создание и сохранение нового экземпляра модели Product
def insert():
    product = Product()
    product.name = "Название продукта"
    product.category = Category.objects.get(
        id=random.randint(10, 18)
    )  # Случайный выбор объекта модели Category из базы данных
    product.style = Style.objects.get(
        id=random.randint(10, 18)
    )  # Случайный выбор объекта модели Style из базы данных
    product.brand = Brand.objects.get(
        id=random.randint(1, 8)
    )  # Случайный выбор объекта модели Brand из базы данных
    product.color = Color.objects.get(
        id=random.randint(1, 5)
    )  # Случайный выбор объекта модели Color из базы данных
    product.size = Size.objects.get(
        id=random.randint(1, 7)
    )  # Случайный выбор объекта модели Size из базы данных
    product.vendor_code = "ABC" + str(
        random.randint(100, 999)
    )  # Генерация случайного значения для поля vendor_code
    product.collection = "Коллекция продукта"
    product.price = round(
        random.uniform(1, 1000), 2
    )  # Генерация случайного значения для поля price
    product.description = "Описание продукта"
    product.image1 = "image1.jpg"
    product.image2 = "image2.jpg"
    product.image3 = "image3.jpg"
    product.image4 = "image4.jpg"
    product.sale = random.choice(
        [True, False]
    )  # Случайный выбор значения для поля sale
    product.created_at = (
        datetime.now()
    )  # Установка текущей даты и времени для поля created_at
    product.save()  # Сохранение объекта в базе данных
