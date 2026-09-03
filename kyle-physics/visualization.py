
import matplotlib.pyplot as plt
from physics import calculate_hail_physics
from probability import damage_probability

def plot_probability_curve(inputs, material_data):
    hail_sizes = []
    probabilities = []

    # simulate hail sizes from 0.5 inch to 4 inches
    for size in [x * 0.1 for x in range(5, 41)]:
        physics = calculate_hail_physics(size)
        energy = physics["energy"]

        prob = damage_probability(inputs, energy, material_data)

        hail_sizes.append(size)
        probabilities.append(prob)

    plt.plot(hail_sizes, probabilities)

    plt.title("Hail Size vs Damage Probability")
    plt.xlabel("Hail Diameter (inches)")
    plt.ylabel("Damage Probability")

    plt.ylim(0, 1)

    plt.show()

def plot_energy_histogram(results):

    energies = [
        storm["impact_energy"]
        for storm in results
    ]

    plt.hist(energies, bins=30)

    plt.title("Impact Energy Distribution")

    plt.xlabel("Energy (J)")

    plt.ylabel("Frequency")

    plt.show()

def plot_probability_histogram(results):

    probabilities = [
        storm["probability"]
        for storm in results
    ]

    plt.hist(probabilities, bins=20)

    plt.title("Damage Probability Distribution")

    plt.xlabel("Probability")

    plt.ylabel("Frequency")

    plt.show()

def plot_probability_vs_hail(results):

    hail = [
        storm["hail_size"]
        for storm in results
    ]

    probabilities = [
        storm["probability"]
        for storm in results
    ]

    plt.scatter(hail, probabilities)

    plt.xlabel("Hail Size")

    plt.ylabel("Damage Probability")

    plt.title("Damage Probability vs Hail Size")

    plt.show()

