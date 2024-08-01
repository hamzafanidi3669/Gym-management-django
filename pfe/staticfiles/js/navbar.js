// Ensure the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Show Menu Functionality
    const showMenu = (toggleId, navId) => {
        const toggle = document.getElementById(toggleId),
              nav = document.getElementById(navId);

        if (toggle && nav) {
            toggle.addEventListener('click', () => {
                // Toggle show-menu class
                nav.classList.toggle('show-menu');

                // Toggle show-icon class
                toggle.classList.toggle('show-icon');
            });
        }
    };

    showMenu('nav-toggle', 'nav-menu');

    // Active Link Functionality
    const navLinks = document.querySelectorAll('.nav__link');
    const currentUrl = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
        }
    });
});