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

// Cagnotte : montant, objectif et donateurs lus dans assets/cagnotte.json,
// que GitHub met à jour toutes les 6 heures à partir de la page GoFundMe
const CAGNOTTE_URL = new URL("cagnotte.json", document.currentScript.src);
const XAF_PER_EUR = 655.957;

async function showFundraising() {
  const goal = document.getElementById("goal");
  if (!goal) return;
  let data;
  try {
    data = await (await fetch(CAGNOTTE_URL, { cache: "no-cache" })).json();
  } catch {
    return; // sans données, on garde le message d'origine
  }
  const locale = EN ? "en-GB" : "fr-FR";
  const fmt = (n) => Math.round(n).toLocaleString(locale);
  const percent = Math.min(100, Math.round((data.raised / data.goal) * 100));
  const fcfa = Math.round((data.goal * XAF_PER_EUR) / 1000) * 1000;

  goal.querySelector(".goal-amount").textContent = fmt(data.goal);
  goal.querySelector(".goal-fcfa").textContent = EN ? "about " + fmt(fcfa) + " FCFA" : "soit environ " + fmt(fcfa) + " FCFA";
  goal.querySelector(".progress").hidden = false;
  goal.querySelector(".goal-first").hidden = true;

  const bar = goal.querySelector(".bar");
  bar.setAttribute("aria-valuemax", data.goal);
  bar.setAttribute("aria-valuenow", data.raised);
  bar.firstElementChild.style.width = percent + "%";

  const donors = data.donors;
  let text;
  if (!data.raised) {
    text = EN
      ? "€0 raised of €" + fmt(data.goal) + ": be the first to give!"
      : "0 € récoltés sur " + fmt(data.goal) + " € : soyez le premier donateur !";
  } else if (EN) {
    text = "€" + fmt(data.raised) + " raised of €" + fmt(data.goal) + " (" + percent + "%)" +
      (donors ? " from " + donors + " donor" + (donors > 1 ? "s" : "") : "") + ". Thank you!";
  } else {
    text = fmt(data.raised) + " € récoltés sur " + fmt(data.goal) + " € (" + percent + " %)" +
      (donors ? " grâce à " + donors + " donateur" + (donors > 1 ? "s" : "") : "") + ". Merci !";
  }
  goal.querySelector(".progress-text").textContent = text;
}

showOpeningStatus();
setUpMenu();
setUpMap();
showFundraising();
