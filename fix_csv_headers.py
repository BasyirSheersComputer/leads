#!/usr/bin/env python3
"""
Fix CSV headers - separate email and contact info into proper columns
"""
import csv
import re

# Read the current CSV
leads = []
print("\nReading CSV file...")
with open('originistudios_leads.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        leads.append(row)

print(f"Read {len(leads)} leads from file")

if len(leads) == 0:
    print("ERROR: No leads found in file!")
    exit(1)

print("\n" + "="*100)
print("FIXING CSV HEADERS - SEPARATING EMAIL AND CONTACT INFO")
print("="*100 + "\n")

# Process each lead to extract email and reorganize
new_leads = []
for lead in leads:
    # Extract email from Notes field
    email = ""
    notes = lead.get('Notes', '')
    if 'Email:' in notes:
        # Extract the email using regex
        email_match = re.search(r'Email:\s*([^\s|]+)', notes)
        if email_match:
            email = email_match.group(1).strip()
            # Remove email from notes
            notes = re.sub(r'\s*\|\s*Email:[^|]*', '', notes).strip()
    
    # Create new lead dict with reorganized fields
    new_lead = {
        'No.': lead.get('No.', ''),
        'Company Name': lead.get('Company Name', ''),
        'Type': lead.get('Type', ''),
        'Industry': lead.get('Industry', ''),
        'Estimated Location': lead.get('Estimated Location', ''),
        'Phone': lead.get('Contact', ''),  # Renamed from Contact
        'Email': email,
        'Website': lead.get('Website', ''),
        'Source': lead.get('Source', ''),
        'Notes': notes
    }
    new_leads.append(new_lead)

print(f"Processed {len(new_leads)} leads")

# Define new column order
new_fieldnames = [
    'No.',
    'Company Name',
    'Type',
    'Industry',
    'Estimated Location',
    'Phone',
    'Email',
    'Website',
    'Source',
    'Notes'
]

# Write updated CSV with new structure
with open('originistudios_leads.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=new_fieldnames)
    writer.writeheader()
    writer.writerows(new_leads)

print(f"\n✓ Updated {len(new_leads)} leads")
print("✓ Separated Email into dedicated column")
print("✓ Renamed 'Contact' to 'Phone' for clarity")
print("✓ Reorganized columns for better readability")
print("\nNew Column Order:")
for i, field in enumerate(new_fieldnames, 1):
    print(f"  {i}. {field}")

print("\n" + "="*100)
print("✓ CSV file updated: originistudios_leads.csv")
print("="*100 + "\n")

# Show sample of first 5 leads
print("SAMPLE DATA (First 5 leads):")
print("="*100 + "\n")
for i, lead in enumerate(new_leads[:5], 1):
    print(f"{i}. {lead['Company Name']}")
    print(f"   Phone:    {lead['Phone']}")
    print(f"   Email:    {lead['Email']}")
    print(f"   Website:  {lead['Website']}")
    print()

print("✓ File successfully updated!\n")
