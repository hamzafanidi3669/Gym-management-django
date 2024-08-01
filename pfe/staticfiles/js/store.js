document.addEventListener('DOMContentLoaded', function() {
    // Function to load all products initially
    loadAllProducts();

    // Event listener for main category navigation items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            let category = this.getAttribute('data-category');
            loadProducts(category);
        });
    });

    // Event listener for dropdown sub-category items
    document.querySelectorAll('.sub-category-link').forEach(subItem => {
        subItem.addEventListener('click', function(event) {
            // event.preventDefault();
            let subCategory = this.getAttribute('data-subcategory');
            loadProducts(subCategory);
        });
    });

    // Function to load all products
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

    // Function to load products based on category or sub-category using AJAX
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
