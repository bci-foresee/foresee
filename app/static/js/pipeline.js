document.addEventListener("DOMContentLoaded", function() {
    const textElement = document.getElementById("selectedPipeline");
    const textContent = textElement.textContent.replace(/_/g, " ");
    textElement.textContent = textContent;
});

// Makes the customPath option visible if selected.
document.addEventListener("DOMContentLoaded", function() {
    const customElement = document.getElementById("custom");

    if (customElement) {
        customElement.addEventListener("change", function() {
            var customPathDiv = document.getElementById("customPath");
            if (this.checked) {
                customPathDiv.style.display = "block";
            } else {
                customPathDiv.style.display = "none";
            }
        });
    } else {
        console.error("Element with ID 'custom' not found.");
    }

    const carouselImages = document.querySelector('.carousel-images');
    let currentIndex = 0;
    const imageCount = carouselImages.children.length;

    function nextImage() {
      currentIndex = (currentIndex + 1) % imageCount;
      carouselImages.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    function prevImage() {
      currentIndex = (currentIndex - 1 + imageCount) % imageCount;
      carouselImages.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    // Example: Automatically slide to the next image every 3 seconds
    setInterval(nextImage, 3000);
});