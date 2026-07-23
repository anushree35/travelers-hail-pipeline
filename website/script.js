const revealElements = document.querySelectorAll(".reveal");

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
    }
  });
});

revealElements.forEach((el) => observer.observe(el));
 
const streak = document.getElementById("streak");

function updateStreak() {
  const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
  const scrollPercent = scrollableHeight > 0 ? window.scrollY / scrollableHeight : 0;

  const top = -10 + scrollPercent * 120;
  const left = 110 - scrollPercent * 120;

  streak.style.top = top + "%";
  streak.style.left = left + "%";
}

window.addEventListener("scroll", updateStreak);
updateStreak();

const rainContainer = document.getElementById("rain");
const dropCount = 10;

for (let i = 0; i < dropCount; i++) {
  const drop = document.createElement("div");
  drop.className = "rain-drop";
  drop.style.left = Math.random() * 100 + "%";
  drop.style.height = 15 + Math.random() * 25 + "px";
  drop.style.opacity = 0.15 + Math.random() * 0.35;
  drop.style.animationDuration = 3 + Math.random() * 5 + "s";
  drop.style.animationDelay = -Math.random() * 8 + "s";
  rainContainer.appendChild(drop);
}
