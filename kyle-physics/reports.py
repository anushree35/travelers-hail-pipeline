def generate_report(impact_energy, probability, classification):
    print("---------------------------------------------")
    print(f"Impact Energy: {impact_energy:.2f} J")
    print(f"Damage Probability: {probability:.3f}")
    print(f"Damage Level: {classification}")
    print("---------------------------------------------")


def classify_damage(probability):
    if probability < 0.30:
        return "Low Risk"
    elif probability < 0.70:
        return "Moderate Risk"
    else:
        return "High Risk"
