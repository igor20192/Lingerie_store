// Wait for the DOM to be loaded
document.addEventListener("DOMContentLoaded", () => {
    // Get the element with id="brand"
    const brandElement = document.getElementById('brand');
    const catalogElement = document.getElementById('catalog');
    const findElement = document.getElementById('group1');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    // Get the element with id="brand-dropdown"
    const brandDropdownElement = document.getElementById('brand-dropdown');
    const megamenuElement = document.getElementById('megamenu');

    // Add an event listener for mouseenter on the element with id="brand"
    brandElement.addEventListener('mouseenter', function () {
        // Show the dropdown menu on mouseenter
        brandDropdownElement.classList.add('show');
    });

    // Add an event listener for mouseleave on the element with id="brand-dropdown"
    brandDropdownElement.addEventListener('mouseleave', function () {
        // Hide the dropdown menu on mouseleave
        brandDropdownElement.classList.remove('show');
    });

    // Add an event listener for mouseenter on the element with id="catalog"
    catalogElement.addEventListener('mouseenter', () => {
        // Show the megamenu on mouseenter
        megamenuElement.classList.add('show');
    });

    // Add an event listener for mouseleave on the element with id="megamenu"
    megamenuElement.addEventListener('mouseleave', () => {
        // Hide the megamenu on mouseleave
        megamenuElement.classList.remove('show');
    });

    // Add an event listener for click on the element with id="group1"
    findElement.addEventListener('click', () => {
        if (searchInput.style.display === 'none') {
            // Show the search input field if it is hidden
            searchInput.style.display = 'block';
        } else {
            // Hide the search input field and clear search results
            searchInput.style.display = 'none';
            searchResults.innerHTML = '';
        }
    });

    // Add an event listener for input on the search input field
    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value;
        if (searchTerm.trim() === '') {
            // If the search term is empty, clear search results and return
            searchResults.innerHTML = '';
            return;
        }

        // Send an AJAX request to the server with the entered search term
        fetch(`/search/?q=${encodeURIComponent(searchTerm)}`)
            .then(response => response.json())
            .then(data => {
                // Process the response data and display search results
                const resultsHtml = data.map(item => `<li><a href="/product/${item.id}/">${item.name}</a></li>`).join('');
                searchResults.innerHTML = `<ul>${resultsHtml}</ul>`;
            })
            .catch(error => {
                // Handle errors in the AJAX request
                console.error('Error executing AJAX request:', error);
            });
    });
});
