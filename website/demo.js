const BACKEND_URL = "https://travelers-hail-pipeline.onrender.com";

const assessBtn = document.getElementById("assessBtn");
const photoInput = document.getElementById("photoInput");
const demoResult = document.getElementById("demoResult");

if (assessBtn) {
  assessBtn.addEventListener("click", async () => {
    const file = photoInput.files[0];

    if (!file) {
      demoResult.textContent = "Choose a photo first.";
      demoResult.classList.add("visible");
      return;
    }

    const formData = new FormData();
    formData.append("photo", file);

    demoResult.textContent = "Analyzing photo...";
    demoResult.classList.add("visible");
    assessBtn.disabled = true;

    try {
      const response = await fetch(`${BACKEND_URL}/assess`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        demoResult.textContent = `Error: ${data.error}`;
      } else {
        demoResult.textContent = data.result;
      }
    } catch (err) {
      demoResult.textContent =
        "Couldn't reach the backend right now. The example output below shows real results from a previous run.";
    } finally {
      assessBtn.disabled = false;
    }
  });
}
