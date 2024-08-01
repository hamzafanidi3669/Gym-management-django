document.addEventListener("DOMContentLoaded", function() {
  const testimonialContainer = document.querySelector(".testimonial-container");
  const testimonials = document.querySelectorAll(".testimonial");

  let index = 0;
  setInterval(() => {
    index++;
    if (index >= testimonials.length) {
      index = 0;
      testimonialContainer.style.transform = `translateX(0)`;
    } else {
      testimonialContainer.style.transform = `translateX(-${index * 300}px)`; // Ajuster la largeur du défilement
    }
  }, 9000); // Ajuster la durée pour chaque témoignage
});
