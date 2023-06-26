document.addEventListener('DOMContentLoaded', () => {
    let cartScript = document.getElementById('cart-script');

    let itemsId = JSON.parse(cartScript.dataset.items);

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function cartTotal(items) {
        let cartTotalElement = document.getElementById('price_total');
        let total = 0;
        for (const element of items) {
            let subtotalElement = document.getElementById('subtotal_' + element[0]);
            let subtotal = parseFloat(subtotalElement.textContent.replace(/[^\d.]/g, ''));
            total += subtotal;
            cartTotalElement.innerHTML = `Итого: ${total.toFixed(2)}₽`;

        };
    };

    function updateCartQuantity(data) {
        fetch('/cart_quantity_update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(result => {
                // Обработка ответа от сервера
                console.log(result);
            })
            .catch(error => {
                // Обработка ошибок
                console.error(error);
            });
    }


    for (const element of itemsId) {
        let minusButton = document.getElementById('button_minus_' + element[0]);
        let plusButton = document.getElementById('button_plus_' + element[0]);
        let quantityInput = document.getElementById('input_' + element[0]);
        let subtotalElement = document.getElementById('subtotal_' + element[0]);
        let priceElement = document.getElementById('price_' + element[0]);
        let stock = element[1];
        console.log(subtotalElement.textContent);

        minusButton.addEventListener('click', () => {
            if (quantityInput.value > 1) {
                quantityInput.value--;
                subtotalElement.innerHTML = `${(quantityInput.value * priceElement.textContent.slice(0, -1)).toFixed(2)}₽`;
                cartTotal(itemsId);

                let data = {
                    index: element[0],
                    quantity: quantityInput.value
                };

                updateCartQuantity(data)
            }
        });
        plusButton.addEventListener('click', () => {
            if (quantityInput.value < stock) {
                quantityInput.value++;
                subtotalElement.innerHTML = `${(quantityInput.value * priceElement.textContent.slice(0, -1)).toFixed(2)}₽`;
                cartTotal(itemsId)

                let data = {
                    index: element[0],
                    quantity: quantityInput.value
                };

                updateCartQuantity(data)
            }
        });

    }
});