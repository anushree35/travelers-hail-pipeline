

from reports import *
from visualization import *
from simulation import *

from probability import *

from data_export import export_results_to_csv
from ai import analyze_image


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
# MAIN PROGRAM
#----------------------------

def main():
    choice = input(

        "1 - Manual Input\n"

        "2 - Image Analysis\n"

    )

    if choice == "1":

        inputs = get_inputs()

    elif choice == "2":

        image_path = input(

            "Enter image path: "

        )

        ai_features = analyze_image(image_path)
        material_age = int(input("Roof Age (years): "))
        roof_slope = float(input("Roof Slope: "))
        temperature = int(input("Temperature (°F): "))
        num_impacts = int(input("Estimated Number of Impacts: "))
        inputs = {

            "material": ai_features["material"],

            "material_age": material_age,

            "hail_diameter": ai_features["estimated_hail_size"],

            "roof_slope": roof_slope,

            "temperature": temperature,

            "num_impacts": num_impacts,

            "dent_shape": ai_features["dent_shape"],

            "damage_distribution": ai_features["damage_distribution"],

            "dent_depth": ai_features["dent_depth"],

            "dent_diameter": ai_features["dent_diameter"]

        }


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

    plot_probability_curve(inputs, material_data)

    results = monte_carlo_simulation(
        material_data,
        n=1000
    )
    export_results_to_csv(results)

    print_monte_carlo_results(results)

    plot_energy_histogram(results)

    plot_probability_histogram(results)

    plot_probability_vs_hail(results)

    material_results = compare_materials_monte_carlo(1000)

    print_material_rankings(material_results)




if __name__ == "__main__":
    main()
