// Wait for DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Get the element with id="cart-script"
    let cartScript = document.getElementById('cart-script');

    // Parse the value of the "data-items" attribute and convert it to an array itemsId
    let itemsId = JSON.parse(cartScript.dataset.items);

    // Function to get the value of a cookie by name
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

    // Function to calculate and display the total price of items in the cart
    function cartTotal(items) {
        let cartTotalElement = document.getElementById('price_total');
        let total = 0;
        for (const element of items) {
            let subtotalElement = document.getElementById('subtotal_' + element[0]);
            let subtotal = parseFloat(subtotalElement.textContent.replace(/[^\d.]/g, ''));
            total += subtotal;
            cartTotalElement.innerHTML = `Итого: ${total.toFixed(2)}₽`;
        }
    }

    // Function to send an AJAX request for updating the quantity of items in the cart
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
                // Handling the response from the server
                console.log(result);
            })
            .catch(error => {
                // Handling errors
                console.error(error);
            });
    }

    // Handling cart items
    for (const element of itemsId) {
        // Get buttons and input fields for each cart item
        let minusButton = document.getElementById('button_minus_' + element[0]);
        let plusButton = document.getElementById('button_plus_' + element[0]);
        let quantityInput = document.getElementById('input_' + element[0]);
        let subtotalElement = document.getElementById('subtotal_' + element[0]);
        let priceElement = document.getElementById('price_' + element[0]);
        let stock = element[1];

        // Add event listener for the "minusButton" click
        minusButton.addEventListener('click', () => {
            if (quantityInput.value > 1) {
                quantityInput.value--;
                subtotalElement.innerHTML = `${(quantityInput.value * priceElement.textContent.slice(0, -1)).toFixed(2)}₽`;
                cartTotal(itemsId);

                let data = {
                    index: element[0],
                    quantity: quantityInput.value
                };

                updateCartQuantity(data);
            }
        });

        // Add event listener for the "plusButton" click
        plusButton.addEventListener('click', () => {
            if (quantityInput.value < stock) {
                quantityInput.value++;
                subtotalElement.innerHTML = `${(quantityInput.value * priceElement.textContent.slice(0, -1)).toFixed(2)}₽`;
                cartTotal(itemsId);

                let data = {
                    index: element[0],
                    quantity: quantityInput.value
                };

                updateCartQuantity(data);
            }
        });
    }
});
