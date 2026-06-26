# Travelers Hail Damage Assessment Pipeline

Built for the Travelers Insurance x UConn AI/ML Research Fellowship.

The goal is to automate the first pass of a hail damage claim — figure out how bad the damage is, and flag anything that looks suspicious.

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

1. Does the image have GPS coordinates embedded in it? If not, you can't confirm it was taken at the claimed property.
2. Does it have a timestamp? If not, the photo might have been edited or reused from somewhere else.

It also runs the image through a pretrained neural network (ResNet-18) to extract visual features — these would feed into a fraud classifier once there's real labeled data to train on.

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

The scoring weights are based on general domain knowledge, not real Travelers claim data. Next step is calibrating them with historical data and training an actual classifier for the fraud detection side.
