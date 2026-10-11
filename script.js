
// Menu Hamburger
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

// Close menu if clicked outside
document.addEventListener('click', (event) => {
  if (!menuToggle.contains(event.target) && !navLinks.contains(event.target)) {
    navLinks.classList.remove('active');
  }
});

// Carrousel
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  const slides = document.getElementsByClassName("mySlides");
  const dots = document.getElementsByClassName("dot");

  if (n > slides.length) { slideIndex = 1; }
  if (n < 1) { slideIndex = slides.length; }

  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }

  slides[slideIndex - 1].style.display = "block";
  if (dots.length > 0) {
    dots[slideIndex - 1].className += " active";
  }
}

// Auto-advance carrousel every 5 seconds
setInterval(() => {
  plusSlides(1);
}, 5000);

// Notification Bar
const closeNotification = document.querySelector('.close-notification');
const notificationBar = document.querySelector('.notification-bar');

if (closeNotification && notificationBar) {
  closeNotification.addEventListener('click', () => {
    notificationBar.style.display = 'none';
  });
}

// Chatbot
const chatbotToggle = document.querySelector('.chatbot-toggle');
const chatbotWindow = document.querySelector('.chatbot-window');
const chatbotClose = document.querySelector('.chatbot-close');
const chatbotInput = document.querySelector('.chatbot-input input');
const chatbotSend = document.querySelector('.chatbot-input button');
const chatbotMessages = document.querySelector('.chatbot-messages');

if (chatbotToggle && chatbotWindow) {
  chatbotToggle.addEventListener('click', () => {
    chatbotWindow.classList.toggle('active');
  });
}

if (chatbotClose && chatbotWindow) {
  chatbotClose.addEventListener('click', () => {
    chatbotWindow.classList.remove('active');
  });
}

if (chatbotSend && chatbotInput && chatbotMessages) {
  chatbotSend.addEventListener('click', () => {
    const message = chatbotInput.value.trim();
    if (message) {
      const userMessage = document.createElement('div');
      userMessage.className = 'message user';
      userMessage.textContent = message;
      chatbotMessages.appendChild(userMessage);

      // Auto-reply
      setTimeout(() => {
        const botMessage = document.createElement('div');
        botMessage.className = 'message bot';
        botMessage.textContent = "Merci pour votre message ! Nous vous répondrons bientôt.";
        chatbotMessages.appendChild(botMessage);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
      }, 1000);

      chatbotInput.value = '';
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
  });

  chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      chatbotSend.click();
    }
  });
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href');
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});

// Animate elements on scroll
const animateOnScroll = () => {
  const elements = document.querySelectorAll('.universe, .gp, .feature, .step, .odd, .social-action, .team-section, .panel');
  elements.forEach(element => {
    const elementPosition = element.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;
    if (elementPosition < windowHeight - 100) {
      element.classList.add('visible');
    }
  });
};

// Run animation check on load and scroll
window.addEventListener('load', animateOnScroll);
window.addEventListener('scroll', animateOnScroll);

// Reservation form submission
document.querySelector('form')?.addEventListener('submit', (e) => {
  e.preventDefault();
  alert('Merci pour votre réservation ! Nous vous contacterons bientôt pour confirmer.');
});