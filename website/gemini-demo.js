const BACKEND_URL_GEMINI = "https://travelers-hail-pipeline.onrender.com";

const assessBtnGemini = document.getElementById("assessBtnGemini");
const photoInputGemini = document.getElementById("photoInputGemini");
const demoResultGemini = document.getElementById("demoResultGemini");

function formatGeminiResult(data) {
  const confidencePct = Math.round(data.ai_confidence * 100);
  const probabilityPct = Math.round(data.damage_probability * 100);

  return (
    `Material: ${data.material}\n` +
    `Estimated hail size: ${data.estimated_hail_size.toFixed(2)} in\n` +
    `Dent shape: ${data.dent_shape}  |  Damage distribution: ${data.damage_distribution}\n` +
    `AI confidence: ${confidencePct}%\n\n` +
    `Impact energy: ${data.impact_energy.toFixed(2)} J\n` +
    `Damage probability: ${probabilityPct}%\n` +
    `Risk level: ${data.risk_level}\n\n` +
    `AI summary: ${data.analysis_summary}`
  );
}

if (assessBtnGemini) {
  assessBtnGemini.addEventListener("click", async () => {
    const file = photoInputGemini.files[0];

    if (!file) {
      demoResultGemini.textContent = "Choose a photo first.";
      demoResultGemini.classList.add("visible");
      return;
    }

    const formData = new FormData();
    formData.append("photo", file);

    demoResultGemini.textContent = "Analyzing photo with Gemini...";
    demoResultGemini.classList.add("visible");
    assessBtnGemini.disabled = true;

    try {
      const response = await fetch(`${BACKEND_URL_GEMINI}/assess-gemini`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        demoResultGemini.textContent = `Error: ${data.error}`;
      } else {
        demoResultGemini.textContent = formatGeminiResult(data);
      }
    } catch (err) {
      demoResultGemini.textContent =
        "Couldn't reach the backend right now. Try again in a moment, free-tier hosting can take a while to wake up.";
    } finally {
      assessBtnGemini.disabled = false;
    }
  });
}
