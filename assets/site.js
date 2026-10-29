// Horaires : [ouverture, fermeture] en heures, null = fermé (index 0 = dimanche)
const HOURS = [[10, 22], null, [12, 22], [12, 22], [12, 22], [12, 22], [9, 22]];
const DAY_NAMES = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"];

function showOpeningStatus() {
  const status = document.getElementById("status");
  const now = new Date();
  const day = now.getDay();
  const today = HOURS[day];
  const h = now.getHours() + now.getMinutes() / 60;

  if (status) {
    const text = status.lastElementChild;
    if (today && h >= today[0] && h < today[1]) {
      text.textContent = "Ouvert maintenant · jusqu'à " + today[1] + "h";
    } else {
      status.classList.add("closed");
      let next = (day + 1) % 7;
      while (!HOURS[next]) next = (next + 1) % 7;
      text.textContent = today && h < today[0]
        ? "Fermé · ouvre aujourd'hui à " + today[0] + "h"
        : "Fermé · ouvre " + DAY_NAMES[next] + " à " + HOURS[next][0] + "h";
    }
  }

  const row = document.querySelector('#hours li[data-day="' + day + '"]');
  if (row) {
    row.classList.add("today");
    row.firstElementChild.textContent += " (aujourd'hui)";
  }
}

function setUpMenu() {
  const burger = document.querySelector(".burger");
  const menu = document.getElementById("menu");
  if (!burger || !menu) return;

  const close = () => {
    menu.classList.remove("open");
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", "Ouvrir le menu");
  };
  burger.addEventListener("click", () => {
    const open = menu.classList.toggle("open");
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
  });
  menu.addEventListener("click", (e) => {
    if (e.target.closest("a")) close();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu.classList.contains("open")) {
      close();
      burger.focus();
    }
  });
}

// Carte : chargée seulement après un clic, pour qu'aucun cookie Google ne soit déposé sans accord
function setUpMap() {
  const button = document.getElementById("load-map");
  if (!button) return;
  button.addEventListener("click", () => {
    const map = document.getElementById("map");
    const iframe = document.createElement("iframe");
    iframe.title = "Plan d'accès à Case Game sur Google Maps";
    iframe.loading = "lazy";
    iframe.referrerPolicy = "no-referrer-when-downgrade";
    iframe.src = map.dataset.src;
    map.replaceChildren(iframe);
    iframe.focus();
  });
}

showOpeningStatus();
setUpMenu();
setUpMap();
