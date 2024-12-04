import pandas as pd
import os

# List of file names
file_names = [
    "papers.csv",
    "authors.csv",
    "venues.csv",
    "fields_of_study.csv",
    "paper_author_rel.csv",
    "paper_venue_rel.csv",
    "paper_reference_rel.csv",
    "paper_fos_rel.csv"
]

# Input and output directories
input_dir = r"out"

output_dir = r"out_dedup"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each file
for file_name in file_names:
    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(output_dir, file_name)

    # Check if the file exists
    if not os.path.exists(input_path):
        print(f"Error: File not found -> {input_path}")
        continue

    # Read the CSV file and deduplicate
    print(f"Processing file: {file_name}")
    df = pd.read_csv(input_path)
    df_deduplicated = df.drop_duplicates()
    df_deduplicated.to_csv(output_path, index=False)

    print(f"Processed {file_name}: {len(df)} rows reduced to {len(df_deduplicated)} rows.")

print("Deduplication completed.")
