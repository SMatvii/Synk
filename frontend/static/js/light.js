const body = document.querySelector("body"),
      nav = document.querySelector("nav"),
      mode_toggle = document.querySelector(".dark-light"),
      search_toggle = document.querySelector(".searchToggle"),
      search_field = document.querySelector(".search-field"),
      sidebar_open = document.querySelector(".sidebar-open"),
      sidebar_close = document.querySelector(".sidebar-close");

let get_mode = localStorage.getItem("mode");
if (get_mode && get_mode === "dark-mode") {
    body.classList.add("dark");
}

mode_toggle.addEventListener("click", () => {
    mode_toggle.classList.toggle("active");
    body.classList.toggle("dark");

    if (!body.classList.contains("dark")) {
        localStorage.setItem("mode", "light-mode");
    } else {
        localStorage.setItem("mode", "dark-mode");
    }
});

search_toggle.addEventListener("click", () => {
    search_toggle.classList.toggle("active");
    search_field.classList.toggle("active");
});

sidebar_open.addEventListener("click", () => {
    nav.classList.add("active");
});

sidebar_close.addEventListener("click", () => {
    nav.classList.remove("active");
});

body.addEventListener("click", (e) => {
    let click_element = e.target;

    if (!click_element.classList.contains("sidebar-open") && !click_element.closest(".menu")) {
        nav.classList.remove("active");
    }
});