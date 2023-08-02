document.addEventListener("DOMContentLoaded", () => {
    // Получаем элемент с id="brand"
    const brandElement = document.getElementById('brend');
    const catalogElement = document.getElementById('catalog');
    const findElement = document.getElementById('group1');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');


    // Получаем элемент с id="brand-dropdown"
    const brandDropdownElement = document.getElementById('brand-dropdown');
    const megamenuElement = document.getElementById('megamenu')

    // Добавляем обработчик события при наведении курсора на элемент с id="brand"
    brandElement.addEventListener('mouseenter', function () {
        // При наведении курсора показываем выпадающий список
        brandDropdownElement.classList.add('show');
    });

    // Добавляем обработчик события при уходе курсора с элемента с id="brand"
    brandDropdownElement.addEventListener('mouseleave', function () {
        // При уходе курсора скрываем выпадающий список
        brandDropdownElement.classList.remove('show');
    });

    catalogElement.addEventListener('mouseenter', () => {
        megamenuElement.classList.add('show');
    });

    megamenuElement.addEventListener('mouseleave', () => {
        megamenuElement.classList.remove('show');
    });

    findElement.addEventListener('click', () => {
        if (searchInput.style.display === 'none') {
            searchInput.style.display = 'block';
        }
        else {
            searchInput.style.display = 'none';
            searchResults.innerHTML = ''
        }
    });


    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value;
        if (searchTerm.trim() === '') {
            searchResults.innerHTML = '';
            return;
        }

        // Отправляем AJAX-запрос на сервер с введенным поисковым запросом
        fetch(`/search/?q=${encodeURIComponent(searchTerm)}`)
            .then(response => response.json())
            .then(data => {
                const resultsHtml = data.map(item => `<li><a href="/product/${item.id}/">${item.name}</a></li>`).join('');
                searchResults.innerHTML = `<ul>${resultsHtml}</ul>`;
            })
            .catch(error => {
                console.error('Ошибка при выполнении AJAX-запроса:', error);
            });
    });
});

