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
