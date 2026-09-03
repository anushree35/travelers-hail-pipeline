import random
import statistics
import math
from physics import calculate_hail_physics
from probability import damage_probability
from materials import all_materials

def generate_random_storm():
    storm = {
        "hail_size": random.uniform(0.5, 4.0),
        "material_age": random.randint(1,30),
        "roof_slope": random.uniform(2, 12),
        "temperature": random.randint(10, 90),
        "num_impacts": random.randint(1, 100),
        "dent_shape": random.choice(["Circular", "Irregular"]),
        "damage_distribution": random.choice(["Random", "Linear"]),
        "dent_depth": random.uniform(0, 0.15),
        "dent_diameter": random.uniform(0, 2),
        "storm_id": random.randint(100000, 999999),
    }
    return storm

def simulate_single_storm(storm, material_data):

    physics = calculate_hail_physics(
        storm["hail_size"]
    )

    impact_energy = physics["energy"]

    probability = damage_probability(
        storm,
        impact_energy,
        material_data
    )

    damage = random.random() < probability

    return {

        "hail_size": storm["hail_size"],

        "impact_energy": impact_energy,

        "probability": probability,

        "damage": damage,

        "material_age": storm["material_age"],

        "roof_slope": storm["roof_slope"],

        "temperature": storm["temperature"],

        "num_impacts": storm["num_impacts"],

        "dent_depth": storm["dent_depth"],

        "dent_diameter": storm["dent_diameter"]

    }


def monte_carlo_simulation(material_data, n=1000):
    results = []

    for _ in range(n):
        storm = generate_random_storm()
        result = simulate_single_storm(storm, material_data)
        results.append(result)

    return results

def print_monte_carlo_results(results):
    total = len(results)

    damage_count = sum(
        storm["damage"]
        for storm in results
    )

    damage_rate = damage_count / total

    probabilities = [
        storm["probability"]
        for storm in results
    ]

    energies = [
        storm["impact_energy"]
        for storm in results
    ]

    hail_sizes = [
        storm["hail_size"]
        for storm in results
    ]

    mean_probability = statistics.mean(probabilities)

    std_probability = statistics.stdev(probabilities)

    margin = (
            1.96
            * std_probability
            / math.sqrt(total)
    )

    print("\n==============================")
    print("MONTE CARLO RESULTS")
    print("==============================")

    print(f"Storms Simulated: {total}")

    print(f"Damage Events: {damage_count}")

    print(f"Damage Rate: {damage_rate:.3f}")

    print()

    print(f"Average Hail Size: {statistics.mean(hail_sizes):.2f} in")

    print(f"Average Energy: {statistics.mean(energies):.2f} J")

    print(f"Maximum Energy: {max(energies):.2f} J")

    print(f"Minimum Energy: {min(energies):.2f} J")

    print()

    print(f"Average Probability: {mean_probability:.3f}")

    print(f"Standard Deviation: {std_probability:.3f}")

    print(
        f"95% Confidence Interval: "
        f"{mean_probability - margin:.3f}"
        f" - "
        f"{mean_probability + margin:.3f}"
    )
    print("==============================")


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
