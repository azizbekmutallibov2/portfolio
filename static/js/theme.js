document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector("[data-theme-toggle]");
  if (!toggle) {
    return;
  }

  function currentTheme() {
    return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function applyPressedState() {
    toggle.setAttribute("aria-pressed", currentTheme() === "light" ? "true" : "false");
  }

  applyPressedState();

  toggle.addEventListener("click", function () {
    var next = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try {
      window.localStorage.setItem("theme", next);
    } catch (e) {
      /* localStorage unavailable */
    }
    applyPressedState();
  });
});
