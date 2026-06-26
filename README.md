# Travelers Hail Damage Assessment Pipeline

A computer vision pipeline for assessing hail damage severity and detecting potential fraud
in drone imagery — built as part of the Travelers Insurance x UConn AI/ML Research Fellowship.

---

## What This Does

This project has two components:

### 1. `severity_scorer.py` — Damage Severity Scoring

Takes three inputs about a property and hail event:

| Input | Description |
|-------|-------------|
| Hail size (inches) | Diameter of hailstones during the storm |
| Roof material | `asphalt shingle`, `metal`, `clay tile`, or `concrete tile` |
| Roof age (years) | How old the roof is |

Each factor is scored separately and combined into a total (0–100). That total maps to a
**damage tier from 1 to 5**, along with a plain-English description and a recommended
claims action.

**Run it:**
```bash
python severity_scorer.py
```
This runs five built-in test cases covering the full range of tiers.

---

### 2. `fraud_detection.ipynb` — Fraud Detection Pipeline

A Jupyter notebook that runs two checks on a roof image:

1. **Visual Feature Extraction** — Uses a pretrained ResNet-18 (via PyTorch) to compute
   a 512-dimensional feature vector from the image. This vector can feed into a downstream
   fraud classifier once training data is available.

2. **EXIF Metadata Analysis** — Reads the image's embedded metadata and flags:
   - Missing GPS coordinates (can't confirm the photo was taken at the claimed property)
   - Missing timestamp (suggests metadata was stripped, possibly after editing)
   - Timestamp that predates the claimed storm date

A final fraud risk level (LOW / MEDIUM / HIGH) is computed from the number of flags found.

**Run it:**
```bash
jupyter notebook fraud_detection.ipynb
```
If you don't have a real drone image handy, the notebook auto-generates a placeholder so
you can run the full pipeline end-to-end right away.

---

## Setup

Install dependencies:
```bash
pip install torch torchvision pillow numpy jupyter
```

No GPU required — everything runs on CPU for this demo.

---

## Project Structure

```
travelers-hail-pipeline/
├── severity_scorer.py       # Damage tier scoring script
├── fraud_detection.ipynb    # Fraud detection notebook
└── README.md
```

---

## Author

Anushree Sabade — UConn Computer Science  
AI/ML Research Fellowship, Travelers Insurance Partnership
