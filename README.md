# Eye in the Sky — Hail Damage AI Pipeline

Built for the Travelers Insurance x UConn Talent Incubator Research Fellowship, by Kyle (material physics and damage thresholds) and Anushree (scoring pipeline, AI integration, and website).

Eye in the Sky pairs two systems: a rules-based severity score you can trace tier by tier, and a live AI vision model that verifies hail damage from a real roof photo. Together, they help Travelers triage properties faster after a storm.

**Live site:** [anushree35.github.io/travelers-hail-pipeline](https://anushree35.github.io/travelers-hail-pipeline/)
**Live backend:** [travelers-hail-pipeline.onrender.com](https://travelers-hail-pipeline.onrender.com) (free-tier hosting, may take ~30s to wake up on the first request)

---

## What's in here

### `website/`

The proposal site itself — 4 pages, deployed to GitHub Pages and auto-redeployed on every push to `main` via GitHub Actions (`.github/workflows/pages.yml`).

- **Overview** (`index.html`) — the problem, what Travelers already has, and the competitive landscape
- **The Pipeline** (`pipeline.html`) — fraud detection, real severity scoring output, and Kyle's physics-based Monte Carlo simulation
- **The AI Model** (`ai-model.html`) — how the AI model works, how it was built, a live demo you can actually upload a photo to, and a known limitation we found while testing it
- **Business Case** (`business-case.html`) — the pilot program proposal and the team

### `severity_scorer.py`

Fully rules-based, no AI involved. Takes three inputs:
- Hail size (inches)
- Roof material (asphalt shingle, metal, clay tile, concrete tile)
- Roof age (years)

Each gets a score, they add up, and you get a damage tier from 1 to 5 with a recommended adjuster action. Fully explainable, no black box.

```
python3 severity_scorer.py
```

### `kyle-physics/physics_model.py`

Kyle's physics-based damage model. Calculates real hail impact physics (mass, terminal velocity, impact energy from hailstone diameter, using actual ice density and drag equations), compares that against each material's toughness through a sigmoid probability function, and stress-tests the result across 1,000+ Monte Carlo simulated storms per material to rank real-world risk by roofing material. Damage probabilities are still being calibrated against real historical claims data.

### `backend/app.py`

The Flask API actually powering the live AI demo on the website. Deployed on Render (`render.yaml`). Takes an uploaded roof photo, sends it to a vision-capable model deployed on Azure AI Foundry with a prompt asking it to describe the damage, estimate a severity tier 1–5, and justify that tier — then returns the result as JSON.

```
cd backend
pip3 install -r requirements.txt
python3 app.py
```

Needs a `.env` file (gitignored) with `AZURE_ENDPOINT` and `AZURE_API_KEY` from an Azure AI Foundry deployment.

### `backend/hail_vision.py`

A standalone CLI script that calls the same Azure AI Foundry model directly from the terminal, given a local image path. This was the original proof-of-concept before `app.py` existed — it's **not** connected to the live website, just a local testing/debugging tool.

```
python3 hail_vision.py path/to/photo.jpg
```

### `fraud_detection.py`

Work in progress. Checks a drone photo's metadata for GPS coordinates and a timestamp — a real drone photo should always have both, so a missing one is a red flag. Only flags for review; a human adjuster still makes the final call.

```
python3 fraud_detection.py
```

---

## Notes

Scoring weights and damage probabilities are based on research and physics modeling, not real Travelers claim data yet. The AI model currently works through prompting alone — it hasn't been fine-tuned on real claims. Next step is getting access to a small, anonymized sample of historical claims to calibrate both the physics model's thresholds and fine-tune the AI model on real patterns instead of general knowledge.
