#!/usr/bin/env python3
"""
Extract customer leads from Origin Studios website carousel
"""
import csv

# Manually extracted customer names from the carousel HTML
customers_raw = [
    "Negeri Sembilan Chinese Maternity Association",
    "RMCC",
    "Assunta Integrated Social Services",
    "Mandaya Hospital Kerawang",
    "Pulai Spring",
    "Mawar Medical Centre",
    "Sunway TCM Centre",
    "Seri Botani Hospital",
    "Sunway Fertility Centre (Kuching)",
    "Oriental Melaka Straits Medical Centre",
    "Perak Community Specialist Hospital",
    "Putra Specialist Hospital (Batu Pahat)",
    "Royal Progress Hospital",
    "Assunta Hospital",
    "Kek Lok Si Charitable Hospital",
    "Putra Medical Centre (Alor Setar)",
    "Georgetown Specialist Hospital",
    "Mandaya Royal Hospital Puri",
    "Mahkota Medical Centre",
    "Regency Specialist Hospital",
    "Sungai Long Specialist Hospital",
    "Sunway Home Healthcare",
    "Kota Bharu Medical Centre",
    "Anson Bay Medical Centre",
    "Penang Adventist Hospital",
    "Sunway Medical Centre Velocity",
    "Beacon Hospital",
    "Beacon Oncology Centre (Klang)",
    "Beacon TCM",
    "Bagan Specialist Centre",
    "Daehan Rehabilitation Hospital Putrajaya",
    "Unik Polyclinic",
    "Unik Dental Clinic",
    "UNIK Dental Clinic (Semenyih)",
    "Putra Specialist Hospital (Melaka)",
    "Loh Guan Lye Specialists Centre",
    "Pantai Indah Kapuk Hospital",
    "Mount Miriam Cancer Hospital",
    "Aurelius Hospital",
    "The Tun Hussein Onn National Eye Hospital",
    "CMH Specialist Hospital",
    "Sunway Sanctuary",
    "Andorra Women & Children Hospital",
    "Beacon Oncology Centre (Kuantan)",
    "Alpha IVF Womens Specialists",
    "Alpha Fertility Centre",
    "Fertility Space",
    "Genesis IVF",
    "Northern Heart Hospital Penang",
    "Damai Service Hospital (HQ)",
    "SMCI",
    "SSCD",
    "Alhaya Fertility Centre",
    "SMC Damansara",
    "Picaso Digital Forms",
]

# Remove duplicates and sort
customers = sorted(list(set(customers_raw)))

# Categorize customers
def categorize_customer(name):
    """Determine the type of healthcare facility"""
    name_lower = name.lower()
    
    if 'ivf' in name_lower or 'fertility' in name_lower:
        return 'Fertility/IVF Center'
    elif 'oncology' in name_lower or 'cancer' in name_lower:
        return 'Oncology/Cancer Center'
    elif 'dental' in name_lower:
        return 'Dental Clinic'
    elif 'eye' in name_lower or 'ophthalmology' in name_lower:
        return 'Eye Hospital/Ophthalmology'
    elif 'heart' in name_lower or 'cardiac' in name_lower:
        return 'Cardiac/Heart Hospital'
    elif 'rehabilitation' in name_lower:
        return 'Rehabilitation Hospital'
    elif 'women' in name_lower or 'maternity' in name_lower or 'children' in name_lower:
        return 'Women & Children Hospital'
    elif 'tcm' in name_lower or 'traditional chinese' in name_lower:
        return 'Traditional Chinese Medicine'
    elif 'clinic' in name_lower or 'polyclinic' in name_lower:
        return 'Clinic/Polyclinic'
    elif 'hospital' in name_lower or 'medical centre' in name_lower or 'medical center' in name_lower:
        return 'Hospital/Medical Center'
    elif 'home healthcare' in name_lower or 'sanctuary' in name_lower:
        return 'Home Healthcare/Sanctuary'
    elif 'association' in name_lower or 'service' in name_lower or 'social' in name_lower:
        return 'Healthcare Organization'
    else:
        return 'Healthcare Provider'

def determine_location(name):
    """Try to determine location from name"""
    locations = {
        'Kuching': 'Sarawak, Malaysia',
        'Melaka': 'Melaka, Malaysia',
        'Alor Setar': 'Kedah, Malaysia',
        'Batu Pahat': 'Johor, Malaysia',
        'Penang': 'Penang, Malaysia',
        'Kuantan': 'Pahang, Malaysia',
        'Klang': 'Selangor, Malaysia',
        'Putrajaya': 'Putrajaya, Malaysia',
        'Semenyih': 'Selangor, Malaysia',
        'Damansara': 'Selangor, Malaysia',
        'Velocity': 'Kuala Lumpur, Malaysia',
        'Kerawang': 'West Java, Indonesia',
        'Puri': 'Jakarta, Indonesia',
        'Kapuk': 'Jakarta, Indonesia',
        'Kota Bharu': 'Kelantan, Malaysia',
        'Negeri Sembilan': 'Negeri Sembilan, Malaysia',
        'Perak': 'Perak, Malaysia',
    }
    
    for keyword, location in locations.items():
        if keyword in name:
            return location
    
    # Default locations based on common patterns
    if 'Sunway' in name or 'Assunta' in name or 'Beacon' in name:
        return 'Kuala Lumpur/Selangor, Malaysia'
    elif 'Royal Progress' in name or 'Pantai Indah' in name or 'Mandaya' in name:
        return 'Indonesia'
    else:
        return 'Malaysia'

# Create detailed CSV
with open('originistudios_leads.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'No.',
        'Company Name',
        'Type',
        'Industry',
        'Estimated Location',
        'Source',
        'Contact',
        'Website',
        'Notes'
    ])
    
    for i, customer in enumerate(customers, 1):
        customer_type = categorize_customer(customer)
        location = determine_location(customer)
        
        writer.writerow([
            i,
            customer,
            customer_type,
            'Healthcare',
            location,
            'originistudios.com (Client List)',
            '',  # To be filled
            '',  # To be researched
            'Origin Studios customer - likely uses digital healthcare solutions'
        ])

# Print summary
print("\n" + "="*100)
print(" " * 30 + "ORIGIN STUDIOS - CUSTOMER LEADS")
print("="*100)
print(f"\nTotal Customers Extracted: {len(customers)}")
print(f"Source: originistudios.com (Customer Carousel)\n")
print("="*100)

# Print by category
categories = {}
for customer in customers:
    cat = categorize_customer(customer)
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(customer)

for category in sorted(categories.keys()):
    print(f"\n{category} ({len(categories[category])}):")
    print("-" * 100)
    for customer in sorted(categories[category]):
        location = determine_location(customer)
        print(f"  • {customer:<60} [{location}]")

print("\n" + "="*100)
print(f"✓ Leads saved to: originistudios_leads.csv")
print(f"✓ Total: {len(customers)} unique customers")
print("="*100 + "\n")

# Print full list
print("\nFULL ALPHABETICAL LIST:")
print("="*100)
for i, customer in enumerate(customers, 1):
    print(f"{i:3d}. {customer}")
print("="*100)


