(function () {
  try {
    document.documentElement.classList.remove("no-js");
    document.documentElement.classList.add("js");
    var stored = window.localStorage.getItem("theme");
    if (stored === "dark" || stored === "light") {
      document.documentElement.setAttribute("data-theme", stored);
    }
  } catch (e) {
    /* localStorage unavailable; keep server-rendered default */
  }
})();
