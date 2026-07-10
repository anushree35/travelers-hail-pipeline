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
```
python3 severity_scorer.py
```

### `fraud_detection.py`

Work in progress. The idea is to check a drone photo's hidden metadata for GPS coordinates and a timestamp. A real drone photo should always have both — missing either one is a red flag.

Run it:
```
python3 fraud_detection.py
```

---

## Setup

```
pip3 install pillow
```

---

## Notes

Scoring weights are based on research, not real Travelers claim data. Next step is getting access to historical claims to calibrate the weights and build out the fraud detection side.