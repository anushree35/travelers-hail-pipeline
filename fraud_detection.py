"""
fraud_detection.py
------------------
Checks a drone image for fraud signals using two methods:
1. Extracts visual features using a pretrained ResNet-18
2. Reads the image's EXIF metadata to check for GPS and timestamp
"""

import os
import datetime
import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image, ExifTags


# --- Step 1: Load a sample image ---
# Using a placeholder (random noise) if no real image is provided.
# In practice, swap this path for an actual drone photo.

SAMPLE_IMAGE_PATH = "sample_roof.jpg"

if not os.path.exists(SAMPLE_IMAGE_PATH):
    print("No image found, creating a placeholder...")
    placeholder = Image.fromarray(
        np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    )
    placeholder.save(SAMPLE_IMAGE_PATH)

image = Image.open(SAMPLE_IMAGE_PATH).convert("RGB")
print(f"Image loaded: {SAMPLE_IMAGE_PATH} | Size: {image.size}")


# --- Step 2: Preprocess for ResNet ---
# ResNet expects 224x224 images normalized to ImageNet stats

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

input_tensor = preprocess(image).unsqueeze(0)  # add batch dimension


# --- Step 3: Extract features using pretrained ResNet-18 ---
# We remove the last layer so we get a feature vector instead of a class label

def load_feature_extractor():
    resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    # Strip off the final classification layer
    extractor = torch.nn.Sequential(*list(resnet.children())[:-1])
    extractor.eval()
    return extractor

def extract_features(model, tensor):
    with torch.no_grad():
        features = model(tensor)
    return features.squeeze().numpy()

print("\nLoading ResNet-18...")
model = load_feature_extractor()
features = extract_features(model, input_tensor)
print(f"Feature vector extracted: {features.shape[0]} values")
print(f"  min={features.min():.4f}, max={features.max():.4f}, mean={features.mean():.4f}")


# --- Step 4: Check EXIF metadata for fraud signals ---
# Legitimate drone photos should have GPS coordinates and a timestamp.
# Missing either one is a red flag.

def check_exif_metadata(image_path, claimed_storm_date=None):
    flags = []
    gps_present = False
    timestamp = None

    img = Image.open(image_path)
    exif_data = img._getexif()

    if exif_data is None:
        flags.append("NO_EXIF_DATA: Image has no metadata at all.")
        return {"flags": flags, "gps_present": False, "timestamp": None}

    readable = {
        ExifTags.TAGS.get(tag, tag): val
        for tag, val in exif_data.items()
    }

    # Check for GPS
    if readable.get("GPSInfo"):
        gps_present = True
    else:
        flags.append("MISSING_GPS: No GPS found — can't confirm photo location.")

    # Check for timestamp
    raw_ts = readable.get("DateTimeOriginal") or readable.get("DateTime")
    if raw_ts:
        timestamp = raw_ts
        if claimed_storm_date:
            try:
                photo_date = datetime.datetime.strptime(raw_ts, "%Y:%m:%d %H:%M:%S").date()
                if photo_date < claimed_storm_date:
                    flags.append(
                        f"TIMESTAMP_PREDATES_STORM: Photo taken {photo_date}, "
                        f"but storm claimed on {claimed_storm_date}."
                    )
            except ValueError:
                flags.append("TIMESTAMP_PARSE_ERROR: Couldn't read the timestamp.")
    else:
        flags.append("MISSING_TIMESTAMP: No timestamp — metadata may have been stripped.")

    return {"flags": flags, "gps_present": gps_present, "timestamp": timestamp}


claimed_date = datetime.date(2024, 5, 15)
result = check_exif_metadata(SAMPLE_IMAGE_PATH, claimed_storm_date=claimed_date)

print("\n--- EXIF Metadata Check ---")
print(f"GPS Present : {result['gps_present']}")
print(f"Timestamp   : {result['timestamp']}")
print(f"Flags found : {len(result['flags'])}")
for flag in result["flags"]:
    print(f"  ! {flag}")


# --- Step 5: Final fraud risk level ---

def fraud_risk(metadata_result):
    n = len(metadata_result["flags"])
    if n == 0:
        return "LOW"
    elif n == 1:
        return "MEDIUM"
    else:
        return "HIGH"

risk = fraud_risk(result)

print("\n=== FRAUD RISK REPORT ===")
print(f"Risk Level         : {risk}")
print(f"Metadata Flags     : {len(result['flags'])}")
print(f"Feature Vector Norm: {float(np.linalg.norm(features)):.4f}")
print("(Feature vector ready for downstream classifier)")
print("=========================")
