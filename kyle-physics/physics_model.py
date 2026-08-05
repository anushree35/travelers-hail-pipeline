import math

#----------------------------
# MATERIAL DATABASE
#----------------------------

materials = {

"3-tab Asphalt": {
    "failure_mode": "bruise",
    "damage_type": "functional",
    "threshold": 1.0,
    "relative_hardness": 2,
    "brittleness": 3,
    "damage_sensitivity": 1.0
},

"Architectural Asphalt Shingles": {
    "failure_mode": "bruise",
    "damage_type": "functional",
    "threshold": 1.25,
    "relative_hardness": 3,
    "brittleness": 3,
    "damage_sensitivity": 0.90
},

"Impact Resistant Shingles": {
    "failure_mode": "bruise",
    "damage_type": "functional",
    "threshold": 2.00,
    "relative_hardness": 5,
    "brittleness": 2,
    "damage_sensitivity": 0.60
},

"Standing Seam Steel": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 2.50,
    "relative_hardness": 8,
    "brittleness": 1,
    "damage_sensitivity": 0.55
},

"Corrugated Steel": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 2.25,
    "relative_hardness": 7,
    "brittleness": 2,
    "damage_sensitivity": 0.60
},

"Aluminum Roofing": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.75,
    "relative_hardness": 5,
    "brittleness": 2,
    "damage_sensitivity": 0.80
},

"Copper Roofing": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.50,
    "relative_hardness": 4,
    "brittleness": 2,
    "damage_sensitivity": 0.85
},

"Clay Tile": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 1.50,
    "relative_hardness": 9,
    "brittleness": 10,
    "damage_sensitivity": 0.90
},

"Concrete Tile": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 1.75,
    "relative_hardness": 8,
    "brittleness": 8,
    "damage_sensitivity": 0.75
},

"Slate": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 2.00,
    "relative_hardness": 10,
    "brittleness": 10,
    "damage_sensitivity": 0.90
},

"Wood Shake": {
    "failure_mode": "split",
    "damage_type": "functional",
    "threshold": 1.50,
    "relative_hardness": 4,
    "brittleness": 7,
    "damage_sensitivity": 0.90
}

}

exterior_materials = {

"Aluminum Gutters": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.00,
    "relative_hardness": 6,
    "brittleness": 2,
    "damage_sensitivity": 1.00
},

"Steel Gutters": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.50,
    "relative_hardness": 6,
    "brittleness": 2,
    "damage_sensitivity": 0.75
},

"Vinyl Siding": {
    "failure_mode": "crack",
    "damage_type": "functional",
    "threshold": 1.50,
    "relative_hardness": 4,
    "brittleness": 6,
    "damage_sensitivity": 0.80
},

"Fiber Cement Siding": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 2.00,
    "relative_hardness": 8,
    "brittleness": 8,
    "damage_sensitivity": 0.55
},

"Brick": {
    "failure_mode": "chip",
    "damage_type": "cosmetic",
    "threshold": 2.50,
    "relative_hardness": 9,
    "brittleness": 9,
    "damage_sensitivity": 0.30
},

"Stucco": {
    "failure_mode": "crack",
    "damage_type": "functional",
    "threshold": 1.75,
    "relative_hardness": 7,
    "brittleness": 8,
    "damage_sensitivity": 0.65
}

}

vehicle_materials = {

"Steel Body Panel": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.75,
    "relative_hardness": 8,
    "brittleness": 1,
    "damage_sensitivity": 0.70
},

"Aluminum Body Panel": {
    "failure_mode": "dent",
    "damage_type": "cosmetic",
    "threshold": 1.50,
    "relative_hardness": 6,
    "brittleness": 2,
    "damage_sensitivity": 0.85
},

"Tempered Glass": {
    "failure_mode": "shatter",
    "damage_type": "functional",
    "threshold": 2.50,
    "relative_hardness": 10,
    "brittleness": 10,
    "damage_sensitivity": 0.25
},

"Laminated Windshield": {
    "failure_mode": "crack",
    "damage_type": "functional",
    "threshold": 3.00,
    "relative_hardness": 10,
    "brittleness": 9,
    "damage_sensitivity": 0.20
},

"Plastic Bumper": {
    "failure_mode": "crack",
    "damage_type": "cosmetic",
    "threshold": 2.00,
    "relative_hardness": 5,
    "brittleness": 5,
    "damage_sensitivity": 0.50
},

"Carbon Fiber Panel": {
    "failure_mode": "fracture",
    "damage_type": "functional",
    "threshold": 2.25,
    "relative_hardness": 9,
    "brittleness": 8,
    "damage_sensitivity": 0.40
}

}

all_materials = {}
all_materials.update(materials)
all_materials.update(exterior_materials)
all_materials.update(vehicle_materials)

#----------------------------
# INPUT SECTION
#----------------------------

def get_inputs():
    material = input("Enter a material: ")
    material_age = int(input("Enter Material Age: "))
    hail_diameter = float(input("Enter Hail Diameter in inches: "))
    num_impacts = int(input("Enter Number of Impacts: "))
    roof_slope = float(input("Enter Roof Slope: "))
    temperature = int(input("Enter Temperature in Fahrenheit: "))
    dent_diameter = float(input("Enter Dent Diameter: "))
    dent_depth = float(input("Enter Dent Depth: "))
    dent_shape = input("Enter Dent Shape (Circular, Irregular, etc.): ")
    damage_distribution = input("Describe Damage Distribution: ")

    return {
        "material": material,
        "material_age": material_age,
        "hail_diameter": hail_diameter,
        "num_impacts": num_impacts,
        "roof_slope": roof_slope,
        "temperature": temperature,
        "dent_diameter": dent_diameter,
        "dent_depth": dent_depth,
        "dent_shape": dent_shape,
        "damage_distribution": damage_distribution
    }

#----------------------------
# MATERIAL LOOKUP
#----------------------------

def get_material_data(material_name):
    if material_name not in all_materials:
        print("Material not found")
        exit()

    return all_materials[material_name]

#----------------------------
# PHYSICS CALCULATIONS
#----------------------------

def calculate_hail_physics(hail_diameter_inches):
    radius_m = (hail_diameter_inches * 0.0254) / 2

    hail_mass = (4/3) * math.pi * (radius_m ** 3) * 917

    velocity_ms = math.sqrt(
        (2 * hail_mass * 9.8) /
        (1.225 * math.pi * (radius_m ** 2) * 0.44704)
    )

    impact_energy = 0.5 * hail_mass * velocity_ms ** 2

    return {
        "mass": hail_mass,
        "velocity": velocity_ms,
        "energy": impact_energy
    }



#----------------------------
# DAMAGE MODEL
#----------------------------

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


def classify_damage(probability):
    if probability < 0.30:
        return "Low Risk"
    elif probability < 0.70:
        return "Moderate Risk"
    else:
        return "High Risk"

def generate_report(impact_energy, probability, classification):
    print("---------------------------------------------")
    print(f"Impact Energy: {impact_energy:.2f} J")
    print(f"Damage Probability: {probability:.3f}")
    print(f"Damage Level: {classification}")
    print("---------------------------------------------")

#----------------------------
# DATA VISUALIZATION
#----------------------------
import matplotlib.pyplot as plt


def plot_probability_curve(material_data):
    hail_sizes = []
    probabilities = []

    # simulate hail sizes from 0.5 inch to 4 inches
    for size in [x * 0.1 for x in range(5, 41)]:
        physics = calculate_hail_physics(size)
        energy = physics["energy"]

        prob = damage_probability(energy, material_data)

        hail_sizes.append(size)
        probabilities.append(prob)

    plt.plot(hail_sizes, probabilities)

    plt.title("Hail Size vs Damage Probability")
    plt.xlabel("Hail Diameter (inches)")
    plt.ylabel("Damage Probability")

    plt.ylim(0, 1)

    plt.show()


#----------------------------
# STORM SIMULATION
#----------------------------
import random
def monte_carlo_simulation(material_data, n=1000):
    results = {
        "damage_count": 0,
        "no_damage_count": 0,
        "probabilitis": []
    }

    for _ in range(n):
        hail_size = random.uniform(0.5, 4.0) #random hail size
        simulated_inputs = {
            "material_age": random.randint(1, 30),
            "roof_slope": random.uniform(2, 12),
            "temperature": random.randint(10, 90),
            "num_impacts": random.randint(1, 100),
            "dent_shape": random.choice(
                ["Circular", "Irregular"]
            ),
            "damage_distribution": random.choice(
                ["Random", "Linear"]
            ),
            "dent_depth": random.uniform(0, 0.15),
            "dent_diameter": random.uniform(0, 2)
        }

        physics = calculate_hail_physics(hail_size)
        energy = physics["energy"]
        prob = damage_probability(simulated_inputs,
                                  energy,
                                  material_data
                                  )
        outcome = random.random() , prob

        if outcome:
            results["damage_count"] += 1
        else:
            results["no_damage_count"] += 1

        results["probabilitis"].append(prob)

    return results

def print_monte_carlo_results(results, n):
    damage_rate = results["damage_count"] / n

    print("\n====================================")
    print("MONTE CARLO STORM SIMULATION")
    print("====================================")
    print(f"Total Simulations: {n}")
    print(f"Damage Events: {results['damage_count']}")
    print(f"No Damage Events: {results['no_damage_count']}")
    print(f"Estimated Damage Probability: {damage_rate:.3f}")
    print("====================================\n")

def compare_materials_monte_carlo(n=1000):

    results = {}

    for material_name, material_data in all_materials.items():

        damage_count = 0

        for _ in range(n):

            hail_size = random.uniform(0.5, 4.0)

            simulated_inputs = {
                "material_age": random.randint(1, 30),
                "roof_slope": random.uniform(2, 12),
                "temperature": random.randint(10, 90),
                "num_impacts": random.randint(1, 100),

                "dent_shape": random.choice(
                    ["Circular", "Irregular"]
                ),

                "damage_distribution": random.choice(
                    ["Random", "Linear"]
                ),

                "dent_depth": random.uniform(0, 0.15),

                "dent_diameter": random.uniform(0, 2)
            }

            physics = calculate_hail_physics(hail_size)

            probability = damage_probability(
                simulated_inputs,
                physics["energy"],
                material_data
            )

            if random.random() < probability:
                damage_count += 1

        results[material_name] = damage_count / n

    return results

def print_material_rankings(results):

    print("\n========== MATERIAL RISK RANKINGS ==========\n")

    ranked = sorted(
        results.items(),
        key=lambda x: x[1]
    )

    for material, probability in ranked:

        print(f"{material:<30} {probability:.3f}")


#----------------------------
# MAIN PROGRAM
#----------------------------

def main():
    inputs = get_inputs()

    material_data = get_material_data(inputs["material"])

    physics = calculate_hail_physics(inputs["hail_diameter"])
    impact_energy = physics["energy"]


    prob = damage_probability(
        inputs,
        impact_energy,
        material_data
    )


    level = classify_damage(prob)


    generate_report(impact_energy, prob, level)

    #plot_probability_curve(material_data)

    results = monte_carlo_simulation(material_data, n=1000)
    print_monte_carlo_results(results, 1000)

    material_results = compare_materials_monte_carlo(1000)

    print_material_rankings(material_results)




if __name__ == "__main__":
    main()

# Continue calibrating data to make it more realistic
