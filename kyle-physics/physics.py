import math

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
