const images = document.querySelectorAll(".slider-img");
const texts = document.querySelectorAll(".slider-text");
const controlls = document.querySelectorAll(".controlls");
const buttons = document.querySelectorAll(".slider-button");
let buttonIndex = 0;
let imageIndex = 0;
let textIndex = 0;

function show(index) {
  images[imageIndex].classList.remove("active");
  texts[textIndex].classList.remove("active");
  buttons[buttonIndex].classList.remove("active");

  images[index].classList.add("active");
  texts[index].classList.add("active");
  buttons[index].classList.add("active");

  textIndex = index;
  imageIndex = index;
  buttonIndex = index;
}

controlls.forEach((e) => {
  e.addEventListener("click", (event) => {
    if (event.target.classList.contains("prev")) {
      let index = imageIndex - 1;

      if (index < 0) {
        index = images.length - 1;
      }

      show(index);
    } else if (event.target.classList.contains("next")) {
      let index = imageIndex + 1;
      if (index >= images.length) {
        index = 0;
      }
      show(index);
    }
  });
});

let autoplayInterval;

function startAutoplay() {
  autoplayInterval = setInterval(() => {
    let index = imageIndex + 1;
    if (index >= images.length) {
      index = 0;
    }
    show(index);
  }, 5000); // 5000 milliseconds = 5 seconds
}

function stopAutoplay() {
  clearInterval(autoplayInterval);
}

window.addEventListener("load", () => {
  show(imageIndex);
  startAutoplay(); // Start autoplay on load

  // Stop autoplay when the user interacts with the slider
  controlls.forEach((e) => {
    e.addEventListener("mouseover", stopAutoplay);
    e.addEventListener("mouseout", startAutoplay);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const sliderButtons = document.querySelectorAll(
    ".slider-button.btn.orange_without"
  );

  sliderButtons.forEach((button) => {
    button.addEventListener("click", () => {
      if (button.classList.contains("active")) {
        window.location.href = button.dataset.href; // Получаем `href` из `data-href`
      } else {
        // Убираем атрибут href
        button.removeAttribute("href");
      }
    });
  });
});
