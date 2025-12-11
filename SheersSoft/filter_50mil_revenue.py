import csv
from pathlib import Path

INPUT_FILE = Path("SheersSoft/MAH_Members_Complete_2025.csv")
OUTPUT_FILE = Path("SheersSoft/Hotels_ICP_Target_50Mil_Revenue.csv")

# Constants
OCCUPANCY_RATE = 0.65
DAYS_IN_YEAR = 365

# Average Daily Rate (ADR) Estimates (MYR)
ADR_MAP = {
    "5 Star": 550,
    "4 Star": 320,
    "3 Star": 180,
    "2 Star": 120,
    "1 Star": 100,
    "Orchid": 100,
    "Associate": 150, # Assumption
    "Others": 150     # Assumption
}

DEFAULT_ADR = 150

def parse_rooms(value):
    if not value: return 0
    # Extract digits
    digits = "".join([c for c in str(value) if c.isdigit()])
    return int(digits) if digits else 0

def get_adr(category):
    if not category: return DEFAULT_ADR
    
    # Normalize
    cat_norm = category.strip()
    # Simple partial match if exact key not found?
    # The keys in CSV might be '5 Star', '4 Star' etc from previous script logic.
    
    if cat_norm in ADR_MAP:
        return ADR_MAP[cat_norm]
        
    # Fallback partials
    if "5 Star" in cat_norm: return ADR_MAP["5 Star"]
    if "4 Star" in cat_norm: return ADR_MAP["4 Star"]
    if "3 Star" in cat_norm: return ADR_MAP["3 Star"]
    if "2 Star" in cat_norm: return ADR_MAP["2 Star"]
    
    return DEFAULT_ADR

def main():
    if not INPUT_FILE.exists():
        print(f"Error: {INPUT_FILE} not found.")
        return

    print(f"Reading from {INPUT_FILE}...")
    
    with INPUT_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    qualified_hotels = []
    
    for row in rows:
        rooms = parse_rooms(row.get('rooms', 0))
        category = row.get('category', 'Others')
        
        adr = get_adr(category)
        
        # Formula: Rooms * 365 * Occupancy * ADR
        annual_revenue = rooms * DAYS_IN_YEAR * OCCUPANCY_RATE * adr
        
        if annual_revenue >= 50_000_000: # 50 Million
            # Add enriched data
            row['estimated_revenue'] = f"{annual_revenue:,.2f}"
            row['estimated_adr'] = adr
            row['raw_revenue'] = annual_revenue # for sorting
            qualified_hotels.append(row)
            
    # Sort by revenue desc
    qualified_hotels.sort(key=lambda x: x['raw_revenue'], reverse=True)
    
    # Remove raw field before writing
    for h in qualified_hotels:
        del h['raw_revenue']
        
    print(f"Found {len(qualified_hotels)} hotels with estimated revenue >= RM 50,000,000.")
    
    if not qualified_hotels:
        print("No hotels met the criteria. Check assumptions.")
        return

    # Write output
    fieldnames = list(qualified_hotels[0].keys())
    # Ensure revenue columns are at end or specific place? 
    # Just standard writer is fine.
    
    with OUTPUT_FILE.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(qualified_hotels)
        
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
