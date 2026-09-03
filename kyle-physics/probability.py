import math

def calculate_damage_score(inputs, material_data, impact_energy):
    score = 0

    threshold = material_data["threshold"]

    prob  = damage_probability(impact_energy, material_data)
    score += prob *100

    if inputs["material_age"] > 15:
        score += 15

    if inputs["num_impacts"] > 40:
        score += 10

    if inputs["dent_shape"].lower() == "circular":
        score += 15

    if inputs["damage_distribution"].lower() == "random":
        score += 20

    if inputs["dent_shape"].lower() == "irregular":
        score -= 15

    if inputs["damage_distribution"].lower() == "linear":
        score -= 25

    # physics-based contribution will be improved over time
    score += impact_energy * material_data["damage_sensitivity"] * 0.001

    return score


#R = threshold * relative_hardness / brittleness
def damage_probability(inputs, impact_energy, material_data):
    k = 3.0 #sensitivity scaling can be changed
#resistance in this is an index for how much impact energy a material can withstand
    resistance = (
        material_data["threshold"]
        * material_data["relative_hardness"]
        / material_data["brittleness"]
    )

    severity = impact_energy / resistance
    exponent = -k * (severity - 1)

    base_probability = 1 / (1 + math.exp(exponent))

    # Environment Factors
    age_factor = calculate_age_factor(
        inputs["material_age"]
    )

    slope_factor = calculate_slope_factor(
        inputs["roof_slope"]
    )

    temperature_factor = calculate_temperature_factor(
        inputs["temperature"]
    )

    impact_factor = calculate_impact_factor(
        inputs["num_impacts"]
    )

    # Inspection Evidence

    inspection_factor = calculate_inspection_factor(inputs)

    risk_adjustment = (
        (age_factor - 1)
        + (slope_factor - 1)
        + (temperature_factor - 1)
        + (impact_factor - 1)
        + (inspection_factor - 1)
    )

    final_probability = base_probability + (risk_adjustment * 0.10)
    final_probability = max(0, min(final_probability, 1))
    return final_probability

#-------------------------
# DAMAGE ADJUSTMENT FACTORS
#--------------------------
def calculate_age_factor(material_age):
    if material_age > 15:
        return 1.20
    elif material_age > 8:
        return 1.10
    else:
        return 1.00

def calculate_slope_factor(roof_slope):
    if roof_slope < 4:
        return 1.15

    elif roof_slope < 8:
        return 1.05

    else:
        return 0.90

def calculate_temperature_factor(temperature):
    if temperature < 32:
        return 1.20

    elif temperature < 60:
        return 1.10

    else:
        return 1.00


def calculate_impact_factor(number_of_impacts):
    return 1 + (number_of_impacts / 200)


def calculate_inspection_factor(inputs):
    factor = 1.00

    if inputs["dent_shape"].lower() == "circular":
        factor += 0.10

    if inputs["damage_distribution"].lower() == "random":
        factor += 0.20

    if inputs["dent_depth"] > 0.05:
        factor += 0.15

    if inputs["dent_diameter"] > 1:
        factor += 0.10

    return factor

