document.addEventListener('DOMContentLoaded', () => {
    const showMenu = (toggleId, navId) => {
        const toggle = document.getElementById(toggleId),
              nav = document.getElementById(navId);

        if (toggle && nav) {
            toggle.addEventListener('click', () => {
                nav.classList.toggle('show-menu');

                toggle.classList.toggle('show-icon');
            });
        }
    };

    showMenu('nav-toggle', 'nav-menu');

    const navLinks = document.querySelectorAll('.nav__link');
    const currentUrl = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
        }
    });
});