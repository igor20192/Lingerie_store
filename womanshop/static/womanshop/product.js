document.addEventListener("DOMContentLoaded", () => {
    // Получаем ссылки на изображения
    let image1 = document.getElementById('product_image1');
    let image2 = document.getElementById('product_image2');
    let image3 = document.getElementById('product_image3');
    let image4 = document.getElementById('product_image4');
    // Сохраняем исходный src атрибут image1
    let originalSrc = image1.src;
    // Функция для замены изображения
    function replaceImage(clickedImage) {
        let clickedSrc = clickedImage.src;
        clickedImage.src = image1.src;
        image1.src = clickedSrc;
    }
    // Обработчик клика на изображении image2
    image2.addEventListener('click', function () {
        replaceImage(image2);
    });
    // Обработчик клика на изображении image3
    image3.addEventListener('click', function () {
        replaceImage(image3);
    });
    // Обработчик клика на изображении image4
    image4.addEventListener('click', function () {
        replaceImage(image4);
    });
    // Обработчик клика на изображении image1
    image1.addEventListener('click', function () {
        replaceImage(image1);
    });

    // Получаем ссылки на элементы формы и кнопки
    let productScript = document.getElementById('product-script')
    let quantityForm = document.getElementById('quantity_form');
    let minusButton = document.querySelector('.quantity_button.minus');
    let plusButton = document.querySelector('.quantity_button.plus');
    let quantityInput = document.getElementById('quantity_input');
    let productStock = document.getElementById('product_stock');
    let userIsAuthenticated = productScript.dataset.user;
    let stock = 0;
    let favoriteImage = document.getElementById('favorite');
    const favoriteList = JSON.parse(productScript.dataset.favoritelist);
    console.log(favoriteList);
    const apiURL = document.querySelector("script[src$='product.js']").getAttribute("data-api-url");
    // Функция для получения значения cookie по имени
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (const element of cookies) {
                let cookie = element.trim();
                // Проверяем, является ли cookie искомым cookie по имени
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Функция для обновления доступных размеров
    function updateSizes(sizes) {
        let sizePicker = document.getElementById('size_picker');
        let sizeSquares = sizePicker.getElementsByClassName('size_square');

        // Скрыть все размеры
        Array.from(sizeSquares).forEach(function (square) {
            square.style.display = 'none';
        });

        // Отобразить только выбранные размеры
        sizes.split(',').forEach(function (size) {
            let sizeSquare = sizePicker.querySelector('.size_square[data-size="' + size + '"]');
            if (sizeSquare) {
                sizeSquare.style.display = 'inline-block';
            }
        });
    }


    // Обработчик клика на цветовом кружке
    let colorCircles = document.querySelectorAll('.color_circle');
    colorCircles.forEach(function (circle) {
        circle.addEventListener('click', function () {
            // Убираем класс 'selected' у всех цветовых кружков
            colorCircles.forEach(function (circle) {
                circle.classList.remove('selected');
            });

            // Добавляем класс 'selected' выбранному цветовому кружку
            this.classList.add('selected');

            // Удаляем стиль 'border' у всех цветовых кружков
            colorCircles.forEach(function (circle) {
                circle.style.border = 'none';
            });

            // Добавляем стиль 'border' выбранному цветовому кружку
            this.style.border = '4px solid pink'; // Здесь 'pink' можно заменить на желаемый цвет

            // Получаем доступные размеры для выбранного цвета
            let sizes = this.getAttribute('data-sizes');
            console.log(sizes)


            // Обновляем размеры в соответствующем контейнере
            if (sizes !== null && sizes !== undefined) {
                // Выполнить действия, если размеры не равны null или undefined
                updateSizes(sizes);
            }

        });
    });


    // Обработчик клика на квадратике размера
    // Получаем ссылку на контейнер с квадратиками размеров
    let sizePicker = document.getElementById('size_picker');

    // Получаем ссылки на все квадратики размеров внутри контейнера
    let sizeSquares = sizePicker.getElementsByClassName('size_square');

    // Обработчик клика на квадратике размера
    Array.from(sizeSquares).forEach(function (square) {
        square.addEventListener('click', function () {
            // Убираем класс 'selected' у всех квадратиков размера
            Array.from(sizeSquares).forEach(function (square) {
                square.classList.remove('selected');
            });

            // Добавляем класс 'selected' выбранному квадратику размера
            this.classList.add('selected');

            // Изменяем цвет текста всех квадратиков размера
            Array.from(sizeSquares).forEach(function (square) {
                square.style.color = 'black';
            });

            // Изменяем цвет текста выбранного квадратика размера
            this.style.color = 'pink';

            const productQuantityURL = document.querySelector("#productQuantityURL").value;
            let selectedColor = document.querySelector('.color_circle.selected');
            let selectedSize = document.querySelector('.size_square.selected');
            let color = selectedColor.getAttribute('data-color');
            let size = selectedSize.getAttribute('data-size');
            let data = {
                color: color,
                size: size
            };

            // Создаем и настраиваем XMLHttpRequest объект
            let xhr = new XMLHttpRequest();
            xhr.open('POST', productQuantityURL);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            // Отправляем данные на сервер
            xhr.send(JSON.stringify(data));

            // Обработчик ответа от сервера
            xhr.onload = function () {
                if (xhr.status === 200) {
                    // Обновляем информацию о количестве товара в наличии
                    let response = JSON.parse(xhr.responseText);
                    productStock.textContent = 'В наличии: ' + response.stock;
                    stock = response.stock
                }
            }
        })
    });



    // Обработчик клика на кнопку "-"
    minusButton.addEventListener('click', function () {
        if (quantityInput.value > 1) {
            quantityInput.value--;
        }
    });

    // Обработчик клика на кнопку "+"
    plusButton.addEventListener('click', function () {
        if (quantityInput.value < stock) {
            quantityInput.value++;
        }
    });

    // Обработчик отправки формы
    quantityForm.addEventListener('submit', (event) => {
        event.preventDefault();

        if (userIsAuthenticated === 'True') {
            let selectedColor = document.querySelector('.color_circle.selected');
            let selectedSize = document.querySelector('.size_square.selected');

            // Установка значений выбранного цвета и размера на странице
            let selectedColorText = selectedColor.getAttribute('data-color');
            let selectedSizeText = selectedSize.getAttribute('data-size');
            document.getElementById('product_color').textContent = 'ЦВЕТ: ' + selectedColorText;
            document.getElementById('product_size').textContent = 'РАЗМЕР: ' + selectedSizeText;

            if (selectedColor && selectedSize && quantityInput.value > 0) {
                const productAddCartUrl = document.getElementById('productAddcartUrl').value
                let color = selectedColor.getAttribute('data-color');
                let size = selectedSize.getAttribute('data-size');
                let quantity = quantityInput.value;

                // Создаем объект с данными для отправки на сервер
                let data = {
                    color: color,
                    size: size,
                    quantity: quantity
                };

                // Создаем и настраиваем XMLHttpRequest объект
                let xhr = new XMLHttpRequest();
                xhr.open('POST', productAddCartUrl);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

                // Отправляем данные на сервер
                xhr.send(JSON.stringify(data));

                // Обработчик ответа от сервера
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        // Обновляем информацию о количестве товара в наличии
                        let response = JSON.parse(xhr.responseText);
                        productStock.textContent = 'В наличии: ' + response.stock;
                        quantityInput.value = 1;

                        // Обновляем количество товаров в корзине
                        let itemInCartElement = document.getElementById('item_in_cart');
                        if (itemInCartElement) {
                            let currentItemCount = parseInt(itemInCartElement.textContent);
                            itemInCartElement.textContent = currentItemCount + 1;
                        }


                        // Показываем уведомление об успешном добавлении товара в корзину
                        alert('Товар успешно добавлен в корзину!');
                    } else {
                        // Показываем уведомление об ошибке
                        alert('Ошибка при добавлении товара в корзину!');
                    }
                };
            } else {
                // Показываем уведомление о неправильном выборе цвета, размера или количества
                alert('Пожалуйста, выберите цвет, размер и количество товара!');
            }
        } else {
            alert('Зарегестрируйтесь или войдите!')
        }
    });

    async function getDataProductLove(url, page, paginateBy) {
        const urlWithParams = url + "?" + new URLSearchParams({
            page: page,
            per_page: paginateBy,
            category_by: productScript.dataset.categoryby,
            product_id: productScript.dataset.productid
        })
        const response = await fetch(urlWithParams);
        return response.json();
    }

    class LoadMorePaginatorLove {
        constructor(per_page) {
            this.per_page = per_page
            this.pageIndex = 1
            this.container = document.querySelector('#love')
            this.minusNext = document.querySelector('#minus_next')
            this.plusNext = document.querySelector('#plus_next')
            this.minusNext.addEventListener('click', this.onMinusClickNext.bind(this))
            this.plusNext.addEventListener('click', this.onPlusClickNext.bind(this))
            this.loadLoveMore()
        }

        onMinusClickNext(event) {
            if (this.pageIndex > 1) {
                this.pageIndex--;
                this.loadLoveMore();
            }
        }

        onPlusClickNext(event) {
            this.pageIndex++;
            this.loadLoveMore();
        }

        addLoveElement(product) {
            const div = document.createElement('div');
            let favoriteImageURL = productScript.dataset.favorites;
            if (favoriteList.includes(product.id)) {
                favoriteImageURL = productScript.dataset.life;
            }
            div.innerHTML = `
          <div class="col">
            <img src="${product.image1}"  width="273px" height="364px"  alt="Not photo">
            <img src="${favoriteImageURL}" style="position: relative; top: -350px;
             left: 235px" width="20px" height="18px" alt="Not photo">
            <p>${product.name}</p>
            <p style="color: #F087B6;">${product.brand}</p>
            <p style="font-size: 18px;" width="63px" height="21px">${product.price}₽</p>
            <a href="/product/${product.id}" style="position: relative; color:#C91664; 
            left: 100px; top: -42px" width="73px" height="16px">Подробние</a>
            <p><img src="${productScript.dataset.img}" style="position: relative; 
            left: 100px; top: -15px" alt=""></p>
      `
            this.container.append(div)
            div.style.display = 'block'
        }

        loadLoveMore() {
            getDataProductLove(apiURL, this.pageIndex, this.per_page)
                .then(response => {
                    this.container.innerHTML = '';
                    response.data.forEach((el) => {
                        this.addLoveElement(el)
                    });
                    this.plusNext.style.display = !response.has_next ? "none" : "block";
                    if (this.pageIndex === 1) {
                        this.minusNext.style.display = 'none';
                    }
                    else {
                        this.minusNext.style.display = 'block'
                    }
                });
        }
    }
    new LoadMorePaginatorLove(3);

    function updateFavorite(url) {
        let data = {
            favorite: productScript.dataset.productid
        };
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });
    }

    const addFavoriteUrl = document.querySelector("script[src$='product.js']").getAttribute("data-add-favorite-url");
    const removeFromFavoritesUrl = document.querySelector("script[src$='product.js']").getAttribute("data-remove-favorite-url")

    favoriteImage.addEventListener('click', () => {
        if (favoriteImage.alt !== 'favorite') {
            favoriteImage.src = productScript.dataset.life;
            favoriteImage.alt = 'favorite'
            updateFavorite(addFavoriteUrl);
        }
        else {
            favoriteImage.src = productScript.dataset.favorites;
            favoriteImage.alt = 'not_favorite'
            updateFavorite(removeFromFavoritesUrl);
        }
    });

})