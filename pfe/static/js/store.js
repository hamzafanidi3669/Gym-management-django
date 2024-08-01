document.addEventListener('DOMContentLoaded', function() {
    loadAllProducts();

    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            let category = this.getAttribute('data-category');
            loadProducts(category);
        });
    });

    document.querySelectorAll('.sub-category-link').forEach(subItem => {
        subItem.addEventListener('click', function(event) {
            let subCategory = this.getAttribute('data-subcategory');
            loadProducts(subCategory);
        });
    });

    function loadAllProducts() {
        fetch('/load-products/all/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                document.getElementById('product-grid').innerHTML = data;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    function loadProducts(categoryOrSubCategory) {
        fetch(`/load-products/${categoryOrSubCategory}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                document.getElementById('product-grid').innerHTML = data;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }
});
