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

  var secretTrigger = toggle.querySelector("[data-secret-tap]");
  if (secretTrigger) {
    var tapCount = 0;
    var resetTimer = null;
    var tapThreshold = 7;

    secretTrigger.addEventListener("click", function () {
      tapCount += 1;
      clearTimeout(resetTimer);
      resetTimer = setTimeout(function () {
        tapCount = 0;
      }, 2500);

      if (tapCount >= tapThreshold) {
        tapCount = 0;
        window.location.href = secretTrigger.getAttribute("data-secret-tap");
      }
    });
  }
});
