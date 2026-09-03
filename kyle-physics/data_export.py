import csv

def export_results_to_csv(results, filename="storm_dataset.csv"):

    if len(results) == 0:
        print("No results to export.")
        return

    fieldnames = results[0].keys()

    with open(filename, "w", newline="") as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(results)

    print(f"\nDataset exported to {filename}")


