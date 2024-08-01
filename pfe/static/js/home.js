document.addEventListener("DOMContentLoaded", function() {
  const testimonialContainer = document.querySelector(".testimonial-container");
  const testimonials = document.querySelectorAll(".testimonial");

  let index = 0;
  setInterval(() => {
    index++;
    if (index >= testimonials.length) {
      index = 0;
      // ila fat nombre dyal testimonials kaml donc renitialisih
      testimonialContainer.style.transform = `translateX(0)`;
    } else {
      // largeur dyal temoignage hya 300 px , n9sna mnha l index 
      testimonialContainer.style.transform = `translateX(-${index * 300}px)`; 
    }
  }, 9000); 
});
