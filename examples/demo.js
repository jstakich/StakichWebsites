(function () {
  document.querySelectorAll(".d-slots button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.parentNode.querySelectorAll("button").forEach(function (b) {
        b.classList.remove("is-picked");
      });
      btn.classList.add("is-picked");
    });
  });

  document.querySelectorAll(".d-form").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var msg = form.querySelector(".d-form-msg");
      if (msg) {
        msg.textContent = "This is an example website, so the form doesn't send. Yours would!";
      }
    });
  });
})();
