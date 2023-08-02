document.addEventListener("DOMContentLoaded", () => {
    // Get references to the images
    let image1 = document.getElementById('product_image1');
    let image2 = document.getElementById('product_image2');
    let image3 = document.getElementById('product_image3');
    let image4 = document.getElementById('product_image4');
    // Save the original src attribute of image1
    let originalSrc = image1.src;
    // Function to replace images when clicked
    function replaceImage(clickedImage) {
        let clickedSrc = clickedImage.src;
        clickedImage.src = image1.src;
        image1.src = clickedSrc;
    }
    // Event listeners for images 2, 3, and 4 to swap with image 1

    image2.addEventListener('click', function () {
        replaceImage(image2);
    });

    image3.addEventListener('click', function () {
        replaceImage(image3);
    });

    image4.addEventListener('click', function () {
        replaceImage(image4);
    });
    // Event listener for image 1 to swap back with the original image
    image1.addEventListener('click', function () {
        replaceImage(image1);
    });

    // Get references to form elements and buttons
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
    // Function to get the value of a cookie by name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (const element of cookies) {
                let cookie = element.trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to update the available sizes
    function updateSizes(sizes) {
        let sizePicker = document.getElementById('size_picker');
        let sizeSquares = sizePicker.getElementsByClassName('size_square');

        Array.from(sizeSquares).forEach(function (square) {
            square.style.display = 'none';
        });

        sizes.split(',').forEach(function (size) {
            let sizeSquare = sizePicker.querySelector('.size_square[data-size="' + size + '"]');
            if (sizeSquare) {
                sizeSquare.style.display = 'inline-block';
            }
        });
    }



    let colorCircles = document.querySelectorAll('.color_circle');
    colorCircles.forEach(function (circle) {
        circle.addEventListener('click', function () {
            // Removing the 'selected' class from all color circles
            colorCircles.forEach(function (circle) {
                circle.classList.remove('selected');
            });

            // Adding the 'selected' class to the selected color circle
            this.classList.add('selected');

            // Remove the 'border' style from all color circles
            colorCircles.forEach(function (circle) {
                circle.style.border = 'none';
            });

            // Adding the 'border' style to the selected color circle
            this.style.border = '4px solid pink'; // Here 'pink' can be replaced with the desired color

            // Get the available sizes for the selected color
            let sizes = this.getAttribute('data-sizes');
            console.log(sizes)


            // Update the dimensions in the appropriate container
            if (sizes !== null && sizes !== undefined) {
                // Perform actions if dimensions are not null or undefined
                updateSizes(sizes);
            }

        });
    });


    // Click handler on size square
    // Get a link to a container with size squares
    let sizePicker = document.getElementById('size_picker');

    // Get links to all size squares inside the container
    let sizeSquares = sizePicker.getElementsByClassName('size_square');

    // Click handler on size square
    Array.from(sizeSquares).forEach(function (square) {
        square.addEventListener('click', function () {
            // Remove the 'selected' class from all size squares
            Array.from(sizeSquares).forEach(function (square) {
                square.classList.remove('selected');
            });

            // Adding the 'selected' class to the selected size box
            this.classList.add('selected');

            Array.from(sizeSquares).forEach(function (square) {
                square.style.color = 'black';
            });

            // Change the text color of the selected size box
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

            // Creating and configuring the XMLHttpRequest object
            let xhr = new XMLHttpRequest();
            xhr.open('POST', productQuantityURL);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            // Sending data to the server
            xhr.send(JSON.stringify(data));

            // Server response handler
            xhr.onload = function () {
                if (xhr.status === 200) {
                    // Update information about the quantity of goods in stock
                    let response = JSON.parse(xhr.responseText);
                    productStock.textContent = 'В наличии: ' + response.stock;
                    stock = response.stock
                }
            }
        })
    });



    // Button click handler "-"
    minusButton.addEventListener('click', function () {
        if (quantityInput.value > 1) {
            quantityInput.value--;
        }
    });

    // Button click handler "+"
    plusButton.addEventListener('click', function () {
        if (quantityInput.value < stock) {
            quantityInput.value++;
        }
    });

    // Form submission handler
    quantityForm.addEventListener('submit', (event) => {
        event.preventDefault();

        if (userIsAuthenticated === 'True') {
            let selectedColor = document.querySelector('.color_circle.selected');
            let selectedSize = document.querySelector('.size_square.selected');

            // Setting the values ​​of the selected color and size on the page
            let selectedColorText = selectedColor.getAttribute('data-color');
            let selectedSizeText = selectedSize.getAttribute('data-size');
            document.getElementById('product_color').textContent = 'ЦВЕТ: ' + selectedColorText;
            document.getElementById('product_size').textContent = 'РАЗМЕР: ' + selectedSizeText;

            if (selectedColor && selectedSize && quantityInput.value > 0) {
                const productAddCartUrl = document.getElementById('productAddcartUrl').value
                let color = selectedColor.getAttribute('data-color');
                let size = selectedSize.getAttribute('data-size');
                let quantity = quantityInput.value;

                // Create an object with data to send to the server
                let data = {
                    color: color,
                    size: size,
                    quantity: quantity
                };

                // Creating and configuring the XMLHttpRequest object
                let xhr = new XMLHttpRequest();
                xhr.open('POST', productAddCartUrl);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

                // Sending data to the server
                xhr.send(JSON.stringify(data));

                // Server response handler
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        // Update information about the quantity of goods in stock
                        let response = JSON.parse(xhr.responseText);
                        productStock.textContent = 'В наличии: ' + response.stock;
                        quantityInput.value = 1;

                        // Update the number of items in the cart
                        let itemInCartElement = document.getElementById('item_in_cart');
                        if (itemInCartElement) {
                            let currentItemCount = parseInt(itemInCartElement.textContent);
                            itemInCartElement.textContent = currentItemCount + 1;
                        }


                        // We show a notification about the successful addition of an item to the cart
                        alert('Товар успешно добавлен в корзину!');
                    } else {
                        // Show error notification
                        alert('Ошибка при добавлении товара в корзину!');
                    }
                };
            } else {
                // We show a notification about the wrong choice of color, size or quantity
                alert('Пожалуйста, выберите цвет, размер и количество товара!');
            }
        } else {
            alert('Зарегестрируйтесь или войдите!')
        }
    });

    // Function to fetch more product data (pagination)
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

    // Class for handling product pagination in the "Love" section
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

    // Instantiate the LoadMorePaginatorLove class with 3 products per page
    new LoadMorePaginatorLove(3);

    // Function to update favorite status of a product
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

    // Event listener for the favorite image icon
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