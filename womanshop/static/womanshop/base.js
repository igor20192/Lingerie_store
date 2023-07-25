document.addEventListener("DOMContentLoaded", () => {
    // Получаем элемент с id="brand"
    const brandElement = document.getElementById('brend');

    // Получаем элемент с id="brand-dropdown"
    const brandDropdownElement = document.getElementById('brand-dropdown');

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
})