import csv
from pathlib import Path

def add_unique_id_to_hotels():
    """Add unique ID column to hotels_directory.csv"""
    input_file = Path("hotels_directory.csv")
    output_file = Path("hotels_directory_with_id.csv")
    
    if not input_file.exists():
        raise SystemExit(f"Input file not found: {input_file}")
    
    with input_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Add unique ID as first column
    for i, row in enumerate(rows, 1):
        row['unique_id'] = f"HOTEL_{i:04d}"
    
    # Write updated file with unique_id as first column
    fieldnames = ['unique_id'] + reader.fieldnames
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Added unique IDs to {len(rows)} entries")
    print(f"Output: {output_file}")
    return output_file

if __name__ == "__main__":
    add_unique_id_to_hotels()


