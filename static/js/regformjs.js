let signup = document.querySelector(".signup");
let login = document.querySelector(".login");
let slider = document.querySelector(".slider");
let formSection = document.querySelector(".form-section");
let loginLink = document.querySelector(".login-link");

signup.addEventListener("click", () => {
  slider.classList.add("moveslider");
  formSection.classList.add("form-section-move");
  signup.classList.add("active");
  login.classList.remove("active");
});

login.addEventListener("click", () => {
  slider.classList.remove("moveslider");
  formSection.classList.remove("form-section-move");
  login.classList.add("active");
  signup.classList.remove("active");
});

loginLink.addEventListener("click", (e) => {
  e.preventDefault();
  slider.classList.remove("moveslider");
  formSection.classList.remove("form-section-move");
  login.classList.add("active");
  signup.classList.remove("active");
});
