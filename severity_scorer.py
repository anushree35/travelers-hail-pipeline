"""
severity_scorer.py
Takes hail size, roof material, and roof age as inputs
and outputs a damage tier from 1-5 with a recommended action.
"""

# each material gets a vulnerability score
# asphalt bruises easily, metal is more resistant
MATERIAL_SCORES = {
    "asphalt shingle": 30,
    "metal": 10,
    "clay tile": 20,
    "concrete tile": 15,
}

def hail_size_score(hail_inches):
    if hail_inches < 0.75:
        return 0
    elif hail_inches < 1.0:
        return 10
    elif hail_inches < 1.5:
        return 20
    elif hail_inches < 2.0:
        return 30
    else:
        return 40

def material_score(roof_material):
    key = roof_material.lower().strip()
    return MATERIAL_SCORES.get(key, 20)

def age_score(roof_age_years):
    # older roofs are more vulnerable to the same storm
    if roof_age_years < 5:
        return 5
    elif roof_age_years < 10:
        return 10
    elif roof_age_years < 15:
        return 18
    elif roof_age_years < 20:
        return 24
    else:
        return 30

TIER_INFO = {
    1: {
        "label": "Minimal Damage",
        "description": "Little to no functional damage. Cosmetic impact only.",
        "action": "No claim recommended. Schedule routine inspection.",
    },
    2: {
        "label": "Minor Damage",
        "description": "Surface bruising or granule loss. Roof lifespan slightly reduced.",
        "action": "Document and monitor. Consider preventive maintenance.",
    },
    3: {
        "label": "Moderate Damage",
        "description": "Visible cracking or granule loss. Leaks possible within 1-2 years.",
        "action": "File a claim. Get a professional inspection within 30 days.",
    },
    4: {
        "label": "Significant Damage",
        "description": "Structural integrity affected. Immediate risk of water intrusion.",
        "action": "Expedite claim. Emergency tarping may be needed.",
    },
    5: {
        "label": "Severe Damage",
        "description": "Widespread damage. Full or partial replacement likely required.",
        "action": "Urgent claim. Assign senior adjuster immediately.",
    },
}

def score_to_tier(total_score):
    if total_score <= 15:
        return 1
    elif total_score <= 35:
        return 2
    elif total_score <= 55:
        return 3
    elif total_score <= 75:
        return 4
    else:
        return 5

def assess_damage(hail_inches, roof_material, roof_age_years):
    h = hail_size_score(hail_inches)
    m = material_score(roof_material)
    a = age_score(roof_age_years)

    total = h + m + a
    tier = score_to_tier(total)
    info = TIER_INFO[tier]

    print("=" * 55)
    print(f"  Hail Size     : {hail_inches} inches")
    print(f"  Roof Material : {roof_material.title()}")
    print(f"  Roof Age      : {roof_age_years} years")
    print("-" * 55)
    print(f"  Sub-scores    : hail={h}, material={m}, age={a}")
    print(f"  Total Score   : {total} / 100")
    print("-" * 55)
    print(f"  TIER {tier} — {info['label']}")
    print(f"  {info['description']}")
    print(f"\n  Recommended Action:")
    print(f"  {info['action']}")
    print("=" * 55)
    print()

    return tier


if __name__ == "__main__":
    print("\nRunning test cases...\n")

    assess_damage(0.75, "metal", 3)
    assess_damage(1.25, "asphalt shingle", 12)
    assess_damage(2.0, "asphalt shingle", 22)
    assess_damage(1.75, "clay tile", 14)
    assess_damage(0.5, "concrete tile", 6)
