let btnHamburger = document.querySelector(".hamburger-menu");
let menuMobile = document.querySelector(".menu-mobile");
let closeMenu = document.querySelector(".overlay-menu-mobile");

btnHamburger.addEventListener("click", () => {
  menuMobile.classList.add("active");
});
closeMenu.addEventListener("click", () => {
  menuMobile.classList.remove("active");
});