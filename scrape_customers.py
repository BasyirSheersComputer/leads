import re
import csv
from html.parser import HTMLParser

class CustomerExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.customers = set()
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Extract from data-elementor-lightbox-title
        if 'data-elementor-lightbox-title' in attrs_dict:
            title = attrs_dict['data-elementor-lightbox-title']
            if title:
                self.customers.add(title.replace('&nbsp;', ' ').replace('&amp;', '&'))
        
        # Extract from alt attribute
        if tag == 'img' and 'alt' in attrs_dict:
            alt = attrs_dict['alt']
            if alt and alt.strip():
                self.customers.add(alt.replace('&nbsp;', ' ').replace('&amp;', '&'))

# Read the HTML content
with open('carousel.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Parse and extract
parser = CustomerExtractor()
parser.feed(html_content)

# Remove empty strings and sort
customers = sorted([c for c in parser.customers if c.strip()])

# Save to CSV
with open('originistudios_leads.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Company Name', 'Industry', 'Source'])
    for customer in customers:
        writer.writerow([customer, 'Healthcare', 'originistudios.com'])

print(f"Extracted {len(customers)} unique customers")
print("\nCustomer List:")
for i, customer in enumerate(customers, 1):
    print(f"{i}. {customer}")


