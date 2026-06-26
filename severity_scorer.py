"""
severity_scorer.py
------------------
Hail damage severity scoring for drone imagery pipeline.
Takes hail size, roof material, and roof age as inputs and
outputs a damage tier (1-5) with a recommended claims action.
"""

# --- Scoring Weights ---
# Each factor contributes a sub-score. The sub-scores are summed
# and mapped to a 1-5 tier. Weights were chosen based on insurance
# domain knowledge: larger hail causes exponentially more damage,
# softer materials dent more easily, and older roofs have less
# structural resilience.

# Hail size buckets (inches) → sub-score (0-40 range)
def hail_size_score(hail_inches):
    """
    Returns a sub-score based on hail diameter.
    Industry standard: hail >= 1 inch is considered "damaging."
    """
    if hail_inches < 0.75:
        return 0    # marble-size, cosmetic at most
    elif hail_inches < 1.0:
        return 10   # dime-size, minor damage possible
    elif hail_inches < 1.5:
        return 20   # quarter-size, moderate damage likely
    elif hail_inches < 2.0:
        return 30   # golf ball-size, significant damage
    else:
        return 40   # baseball-size or larger, severe damage


# Material vulnerability scores (0-30 range)
# Asphalt shingles bruise and crack easily; metal and tile are more resistant.
MATERIAL_SCORES = {
    "asphalt shingle": 30,
    "metal": 10,
    "clay tile": 20,
    "concrete tile": 15,
}

def material_score(roof_material):
    """
    Returns a sub-score based on how vulnerable the material is to hail.
    Defaults to mid-range (20) if material is unrecognized.
    """
    key = roof_material.lower().strip()
    return MATERIAL_SCORES.get(key, 20)


# Roof age sub-score (0-30 range)
# Older roofs have degraded granules, brittle sealant, and reduced
# impact resistance — so age compounds damage from any hail event.
def age_score(roof_age_years):
    """
    Returns a sub-score based on roof age in years.
    """
    if roof_age_years < 5:
        return 5    # nearly new, minimal extra risk
    elif roof_age_years < 10:
        return 10
    elif roof_age_years < 15:
        return 18
    elif roof_age_years < 20:
        return 24
    else:
        return 30   # 20+ years, significantly degraded


# --- Tier Mapping ---
# Total possible score: 0 to 100
# We divide that range into 5 tiers.

TIER_INFO = {
    1: {
        "label": "Minimal Damage",
        "description": "Little to no functional damage expected. "
                       "Cosmetic impact only, if any.",
        "action": "No claim recommended. Schedule routine inspection.",
    },
    2: {
        "label": "Minor Damage",
        "description": "Surface bruising or granule loss on shingles. "
                       "Roof lifespan may be slightly reduced.",
        "action": "Document and monitor. Consider preventive maintenance.",
    },
    3: {
        "label": "Moderate Damage",
        "description": "Visible denting, cracking, or granule loss. "
                       "Leaks possible within 1-2 years without repair.",
        "action": "File a claim. Arrange professional inspection within 30 days.",
    },
    4: {
        "label": "Significant Damage",
        "description": "Structural integrity compromised in affected areas. "
                       "Immediate risk of water intrusion.",
        "action": "Expedite claim. Emergency tarping may be needed. "
                  "Prioritize adjuster visit.",
    },
    5: {
        "label": "Severe Damage",
        "description": "Widespread or catastrophic damage. Full or partial "
                       "roof replacement very likely required.",
        "action": "Urgent claim. Assign senior adjuster. "
                  "Authorize emergency repairs immediately.",
    },
}

def score_to_tier(total_score):
    """
    Maps a raw total score (0-100) to a damage tier (1-5).
    Breakpoints are roughly evenly spaced but weighted toward higher tiers
    since under-assessing severe damage is riskier than over-assessing.
    """
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


# --- Main Scoring Function ---

def assess_damage(hail_inches, roof_material, roof_age_years):
    """
    Given hail size (inches), roof material, and roof age (years),
    returns the damage tier (1-5) and prints a full assessment report.
    """
    # Calculate each sub-score
    h_score = hail_size_score(hail_inches)
    m_score = material_score(roof_material)
    a_score = age_score(roof_age_years)

    total = h_score + m_score + a_score
    tier = score_to_tier(total)
    info = TIER_INFO[tier]

    # Print the report
    print("=" * 55)
    print("  HAIL DAMAGE ASSESSMENT REPORT")
    print("=" * 55)
    print(f"  Hail Size     : {hail_inches} inches")
    print(f"  Roof Material : {roof_material.title()}")
    print(f"  Roof Age      : {roof_age_years} years")
    print("-" * 55)
    print(f"  Sub-scores    : hail={h_score}, material={m_score}, age={a_score}")
    print(f"  Total Score   : {total} / 100")
    print("-" * 55)
    print(f"  TIER {tier} — {info['label']}")
    print(f"  {info['description']}")
    print(f"\n  Recommended Action:")
    print(f"  {info['action']}")
    print("=" * 55)
    print()

    return tier


# --- Test Cases ---
# Run this file directly to see output for several representative scenarios.

if __name__ == "__main__":
    print("\nRunning test cases...\n")

    # Case 1: Small hail, new metal roof — expect Tier 1 or 2
    assess_damage(
        hail_inches=0.75,
        roof_material="metal",
        roof_age_years=3
    )

    # Case 2: Moderate hail, mid-age asphalt shingle roof — expect Tier 3
    assess_damage(
        hail_inches=1.25,
        roof_material="asphalt shingle",
        roof_age_years=12
    )

    # Case 3: Large hail, old asphalt shingle roof — expect Tier 5
    assess_damage(
        hail_inches=2.0,
        roof_material="asphalt shingle",
        roof_age_years=22
    )

    # Case 4: Golf ball hail, clay tile, moderately aged — expect Tier 4
    assess_damage(
        hail_inches=1.75,
        roof_material="clay tile",
        roof_age_years=14
    )

    # Case 5: Small hail, concrete tile, newer roof — expect Tier 1
    assess_damage(
        hail_inches=0.5,
        roof_material="concrete tile",
        roof_age_years=6
    )
