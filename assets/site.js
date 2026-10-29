// Horaires : [ouverture, fermeture] en heures, null = fermé (index 0 = dimanche)
const HOURS = [[10, 22], null, [12, 22], [12, 22], [12, 22], [12, 22], [9, 22]];
const EN = document.documentElement.lang === "en";
const DAY_NAMES = EN
  ? ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
  : ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"];

// Heure affichée : « 22h » en français, « 10 pm » en anglais
function hourLabel(h) {
  if (!EN) return h + "h";
  return (h % 12 || 12) + (h < 12 ? " am" : " pm");
}

function showOpeningStatus() {
  const status = document.getElementById("status");
  const now = new Date();
  const day = now.getDay();
  const today = HOURS[day];
  const h = now.getHours() + now.getMinutes() / 60;

  if (status) {
    const text = status.lastElementChild;
    if (today && h >= today[0] && h < today[1]) {
      text.textContent = EN
        ? "Open now · until " + hourLabel(today[1])
        : "Ouvert maintenant · jusqu'à " + hourLabel(today[1]);
    } else {
      status.classList.add("closed");
      let next = (day + 1) % 7;
      while (!HOURS[next]) next = (next + 1) % 7;
      if (EN) {
        text.textContent = today && h < today[0]
          ? "Closed · opens today at " + hourLabel(today[0])
          : "Closed · opens " + DAY_NAMES[next] + " at " + hourLabel(HOURS[next][0]);
      } else {
        text.textContent = today && h < today[0]
          ? "Fermé · ouvre aujourd'hui à " + hourLabel(today[0])
          : "Fermé · ouvre " + DAY_NAMES[next] + " à " + hourLabel(HOURS[next][0]);
      }
    }
  }

  const row = document.querySelector('#hours li[data-day="' + day + '"]');
  if (row) {
    row.classList.add("today");
    row.firstElementChild.textContent += EN ? " (today)" : " (aujourd'hui)";
  }
}

function setUpMenu() {
  const burger = document.querySelector(".burger");
  const menu = document.getElementById("menu");
  if (!burger || !menu) return;

  const close = () => {
    menu.classList.remove("open");
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", EN ? "Open menu" : "Ouvrir le menu");
  };
  burger.addEventListener("click", () => {
    const open = menu.classList.toggle("open");
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open
      ? (EN ? "Close menu" : "Fermer le menu")
      : (EN ? "Open menu" : "Ouvrir le menu"));
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
    iframe.title = EN ? "Map to Case Game on Google Maps" : "Plan d'accès à Case Game sur Google Maps";
    iframe.loading = "lazy";
    iframe.referrerPolicy = "no-referrer-when-downgrade";
    iframe.src = map.dataset.src;
    map.replaceChildren(iframe);
    iframe.focus();
  });
}

// Cagnotte : la barre n'apparaît qu'à partir du premier don
function showFundraising() {
  const goal = document.getElementById("goal");
  if (!goal) return;
  const target = Number(goal.dataset.goal);
  const raised = Number(goal.dataset.raised);
  const donors = Number(goal.dataset.donors);
  if (!raised) return;
  const percent = Math.min(100, Math.round((raised / target) * 100));
  goal.querySelector(".progress").hidden = false;
  goal.querySelector(".goal-first").hidden = true;
  const bar = goal.querySelector(".bar");
  bar.setAttribute("aria-valuenow", raised);
  bar.firstElementChild.style.width = percent + "%";
  goal.querySelector(".progress-text").textContent = EN
    ? "€" + raised.toLocaleString("en-GB") + " raised so far (" + percent + "%)" +
      (donors ? " from " + donors + " donor" + (donors > 1 ? "s" : "") : "") + ". Thank you!"
    : "Déjà " + raised.toLocaleString("fr-FR") + " € récoltés (" + percent + " %)" +
      (donors ? " grâce à " + donors + " donateur" + (donors > 1 ? "s" : "") : "") + ". Merci !";
}

showOpeningStatus();
setUpMenu();
setUpMap();
showFundraising();
