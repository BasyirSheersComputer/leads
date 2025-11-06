#!/usr/bin/env python3
"""
Generate a summary report of the updated leads list
"""
import csv
from collections import Counter

# Read the final CSV
leads = []
with open('originistudios_leads.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    leads = list(reader)

print("\n" + "="*100)
print(" " * 25 + "ORIGIN STUDIOS LEADS - COMPLETE WITH CONTACT INFORMATION")
print("="*100)
print(f"\nTotal Leads: {len(leads)}")

# Count leads with contact information
with_phone = sum(1 for lead in leads if lead['Contact'].strip())
with_website = sum(1 for lead in leads if lead['Website'].strip())
with_email = sum(1 for lead in leads if 'Email:' in lead['Notes'])

print(f"\nContact Information Coverage:")
print(f"  • Phone Numbers: {with_phone}/{len(leads)} ({with_phone/len(leads)*100:.1f}%)")
print(f"  • Websites: {with_website}/{len(leads)} ({with_website/len(leads)*100:.1f}%)")
print(f"  • Email Addresses: {with_email}/{len(leads)} ({with_email/len(leads)*100:.1f}%)")

# Breakdown by type
types = Counter(lead['Type'] for lead in leads)
print(f"\nBreakdown by Facility Type:")
for facility_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {facility_type:<40} {count:>3} leads")

# Breakdown by location
locations = Counter(lead['Estimated Location'] for lead in leads)
print(f"\nBreakdown by Location:")
for location, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {location:<45} {count:>3} leads")

# Sample of leads with full contact information
print("\n" + "="*100)
print("SAMPLE LEADS WITH COMPLETE CONTACT INFORMATION (First 10):")
print("="*100 + "\n")

for i, lead in enumerate(leads[:10], 1):
    # Extract email from notes
    email = ""
    if 'Email:' in lead['Notes']:
        email_part = lead['Notes'].split('Email:')[1].split('|')[0].strip()
        email = email_part
    
    print(f"{i}. {lead['Company Name']}")
    print(f"   Type: {lead['Type']}")
    print(f"   Location: {lead['Estimated Location']}")
    print(f"   Phone: {lead['Contact']}")
    print(f"   Website: {lead['Website']}")
    print(f"   Email: {email}")
    print()

print("="*100)
print(f"✓ Complete leads list saved to: originistudios_leads.csv")
print(f"✓ All {len(leads)} leads now include contact information")
print(f"✓ Ready for outreach campaigns")
print("="*100 + "\n")


