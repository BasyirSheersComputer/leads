import re
import csv

# HTML content from originistudios.com carousel
html_content = """[HTML_PLACEHOLDER]"""

# Extract customer names from data-elementor-lightbox-title attributes
title_pattern = r'data-elementor-lightbox-title="([^"]+)"'
titles = re.findall(title_pattern, html_content)

# Extract customer names from alt attributes
alt_pattern = r'alt="([^"]+)"'
alts = re.findall(alt_pattern, html_content)

# Combine and clean
all_customers = titles + alts
customers = set()

for customer in all_customers:
    # Clean up HTML entities
    cleaned = customer.replace('&nbsp;', ' ').replace('&amp;', '&').strip()
    # Skip empty strings and generic terms
    if cleaned and cleaned not in ['', 'sscd-logo']:
        customers.add(cleaned)

# Sort alphabetically
customers_list = sorted(list(customers))

# Create leads CSV
with open('originistudios_leads.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['#', 'Company Name', 'Industry', 'Type', 'Source', 'Website'])
    
    for i, customer in enumerate(customers_list, 1):
        # Determine type based on name
        if 'Hospital' in customer or 'Medical Centre' in customer or 'Medical Center' in customer:
            type_cat = 'Hospital/Medical Center'
        elif 'Clinic' in customer or 'Polyclinic' in customer:
            type_cat = 'Clinic'
        elif 'IVF' in customer or 'Fertility' in customer:
            type_cat = 'Fertility Center'
        elif 'Oncology' in customer or 'Cancer' in customer:
            type_cat = 'Oncology Center'
        elif 'TCM' in customer:
            type_cat = 'Traditional Chinese Medicine'
        elif 'Association' in customer or 'Service' in customer:
            type_cat = 'Healthcare Organization'
        else:
            type_cat = 'Healthcare Provider'
        
        writer.writerow([i, customer, 'Healthcare', type_cat, 'originistudios.com', ''])

print(f"✓ Extracted {len(customers_list)} unique customers from Origin Studios")
print(f"✓ Saved to: originistudios_leads.csv")
print("\n" + "="*80)
print("CUSTOMER LIST:")
print("="*80)

for i, customer in enumerate(customers_list, 1):
    print(f"{i:2d}. {customer}")

print("="*80)
print(f"\nTotal: {len(customers_list)} leads")


