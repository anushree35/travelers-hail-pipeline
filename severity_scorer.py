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
    1: {"label": "Minimal Damage", "action": "No claim needed. Schedule routine inspection."},
    2: {"label": "Minor Damage", "action": "Document and monitor."},
    3: {"label": "Moderate Damage", "action": "File a claim. Get an inspection within 30 days."},
    4: {"label": "Significant Damage", "action": "Expedite claim. Emergency tarping may be needed."},
    5: {"label": "Severe Damage", "action": "Urgent claim. Assign senior adjuster immediately."},
}

def score_to_tier(total):
    if total <= 15:
        return 1
    elif total <= 35:
        return 2
    elif total <= 55:
        return 3
    elif total <= 75:
        return 4
    else:
        return 5

def assess_damage(hail_inches, roof_material, roof_age_years):
    h = hail_size_score(hail_inches)
    m = material_score(roof_material)
    a = age_score(roof_age_years)
    total = h + m + a
    tier = score_to_tier(total)

    print(f"Hail: {hail_inches}in | Material: {roof_material} | Age: {roof_age_years}yrs")
    print(f"Score: {total}/100 → TIER {tier}: {TIER_INFO[tier]['label']}")
    print(f"Action: {TIER_INFO[tier]['action']}")
    print()

assess_damage(0.75, "metal", 3)
assess_damage(1.25, "asphalt shingle", 12)
assess_damage(2.0, "asphalt shingle", 22)
assess_damage(1.75, "clay tile", 14)
assess_damage(0.5, "concrete tile", 6)