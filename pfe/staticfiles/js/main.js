// main.js

// Fonction pour charger les scripts de manière asynchrone
function loadScript(src) {
    return new Promise((resolve, reject) => {
        let script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

// Liste des scripts à charger
const scripts = [
    '/static/js/pricing/vendor/modernizr-3.5.0.min.js',
    '/static/js/pricing/vendor/jquery-1.12.4.min.js',
    '/static/js/pricing/popper.min.js',
    '/static/js/pricing/bootstrap.min.js',
    '/static/js/pricing/jquery.slicknav.min.js',
    '/static/js/pricing/owl.carousel.min.js',
    '/static/js/pricing/slick.min.js',
    '/static/js/pricing/wow.min.js',
    '/static/js/pricing/animated.headline.js',
    '/static/js/pricing/jquery.magnific-popup.js',
    '/static/js/pricing/gijgo.min.js',
    '/static/js/pricing/jquery.nice-select.min.js',
    '/static/js/pricing/jquery.sticky.js',
    '/static/js/pricing/jquery.counterup.min.js',
    '/static/js/pricing/waypoints.min.js',
    '/static/js/pricing/jquery.countdown.min.js',
    '/static/js/pricing/hover-direction-snake.min.js',
    '/static/js/pricing/contact.js',
    '/static/js/pricing/jquery.form.js',
    '/static/js/pricing/jquery.validate.min.js',
    '/static/js/pricing/mail-script.js',
    '/static/js/pricing/jquery.ajaxchimp.min.js',
    '/static/js/pricing/plugins.js',
    '/static/js/pricing/main.js'
];

// Fonction pour initialiser tous les plugins et fonctionnalités
function initializeAll() {
    // Ici, vous pouvez ajouter l'initialisation de vos plugins
    // Par exemple:
    if ($.fn.slicknav) {
        $('#mobile-menu').slicknav();
    }
    if ($.fn.owlCarousel) {
        $('.owl-carousel').owlCarousel();
    }
    // ... ajoutez d'autres initialisations selon vos besoins
}

// Chargement de tous les scripts
Promise.all(scripts.map(loadScript))
    .then(() => {
        console.log('Tous les scripts sont chargés');
        initializeAll();
    })
    .catch(error => {
        console.error('Erreur lors du chargement des scripts:', error);
    });