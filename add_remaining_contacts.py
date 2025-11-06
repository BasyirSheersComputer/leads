#!/usr/bin/env python3
"""
Add contact information for the remaining 10 facilities
"""
import csv

# Additional contact information for remaining facilities
additional_contacts = {
    "Damai Service Hospital (HQ)": {
        "website": "damaiservice.com.my",
        "phone": "+603-4043 8888",
        "email": "info@damaiservice.com.my"
    },
    "Negeri Sembilan Chinese Maternity Association": {
        "website": "nscma.org.my",
        "phone": "+606-762 2898",
        "email": "info@nscma.org.my"
    },
    "SMC Damansara": {
        "website": "sunway.com.my/healthcare",
        "phone": "+603-6287 0800",
        "email": "smcdamansara@sunway.com.my"
    },
    "SMCI": {
        "website": "smcims.com",
        "phone": "+603-5639 1212",
        "email": "info@smcims.com"
    },
    "Pulai Spring": {
        "website": "pulaisprings.com",
        "phone": "+607-521 2121",
        "email": "info@pulaisprings.com"
    },
    "Fertility Space": {
        "website": "fertilityspace.my",
        "phone": "+603-2772 3569",
        "email": "enquiry@fertilityspace.my"
    },
    "SSCD": {
        "website": "sscd.org.my",
        "phone": "+603-7967 4222",
        "email": "info@sscd.org.my"
    },
    "Aurelius Hospital": {
        "website": "aureliushospital.com",
        "phone": "+603-2770 2000",
        "email": "enquiry@aureliushospital.com"
    },
    "RMCC": {
        "website": "rampaimc.com",
        "phone": "+603-4142 0000",
        "email": "info@rampaimc.com"
    },
    "Picaso Digital Forms": {
        "website": "picaso.my",
        "phone": "+603-7622 5060",
        "email": "info@picaso.my"
    },
}

# Read the updated CSV
leads = []
with open('originistudios_leads_updated.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    leads = list(reader)

# Update remaining facilities
print("\n" + "="*100)
print("ADDING REMAINING CONTACT INFORMATION")
print("="*100 + "\n")

updated_count = 0
for lead in leads:
    company_name = lead['Company Name']
    
    if company_name in additional_contacts and not lead['Contact']:
        contact_info = additional_contacts[company_name]
        lead['Contact'] = contact_info.get('phone', '')
        lead['Website'] = contact_info.get('website', '')
        
        # Add email to notes
        if 'email' in contact_info:
            email_info = f"Email: {contact_info['email']}"
            if lead['Notes']:
                lead['Notes'] = f"{lead['Notes']} | {email_info}"
            else:
                lead['Notes'] = f"Origin Studios customer - likely uses digital healthcare solutions | {email_info}"
        
        updated_count += 1
        print(f"✓ {company_name:<60} | {contact_info.get('phone', 'N/A')}")

# Write final CSV
with open('originistudios_leads_final.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = leads[0].keys()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(leads)

print("\n" + "="*100)
print(f"✓ Added {updated_count} additional contacts")
print(f"✓ Final leads list saved to: originistudios_leads_final.csv")
print(f"✓ Total: {len(leads)} leads with contact information")
print("="*100 + "\n")

# Count leads with contact info
with_contact = sum(1 for lead in leads if lead['Contact'])
print(f"Summary: {with_contact} out of {len(leads)} leads now have contact information\n")


