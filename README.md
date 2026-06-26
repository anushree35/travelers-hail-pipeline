# Travelers Hail Damage Assessment Pipeline

Built for the Travelers Insurance x UConn Research Fellowship.

The goal is to automate the first pass of a hail damage claim, figure out how bad the damage is, and flag anything that looks suspicious.

---

## What's in here

### `severity_scorer.py`

Takes three inputs:
- How big the hail was (in inches)
- What the roof is made of (asphalt shingle, metal, clay tile, concrete tile)
- How old the roof is

Each one gets a score, they add up, and you get a damage tier from 1 to 5 with a recommended action for the adjuster.

Run it:
```bash
python3 severity_scorer.py
```

### `fraud_detection.py`

Takes a drone photo and checks two things:

1. Runs the image through a pretrained ResNet-18 neural network to extract a feature vector — a list of numbers representing what's visually in the image. These feed into a fraud classifier once labeled training data is available.

2. Reads the image's EXIF metadata and flags missing GPS coordinates or a missing timestamp — both of which should always be present in a legitimate drone photo.

Run it:
```bash
python3 fraud_detection.py
```

---

## Setup

```bash
pip3 install torch torchvision pillow numpy
```

---

## Notes

The scoring weights are based on research, not real Travelers claim data. Next step is calibrating them with historical data and training an actual classifier on the fraud detection side. Long term this pipeline will be part of a live demo on the final proposal website.
