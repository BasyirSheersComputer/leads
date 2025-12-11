import csv
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse
from pathlib import Path

INPUT_FILE = Path("SheersSoft/Hotels_ICP_Target_50Mil_Revenue.csv")
OUTPUT_FILE = Path("SheersSoft/Hotels_ICP_Target_50Mil_Verified.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def clean_text(text):
    if not text: return ""
    return " ".join(text.strip().split())

def extract_emails(soup):
    emails = set()
    # Mailto links
    for a in soup.select("a[href^='mailto:']"):
        href = a.get("href", "")
        email = href.replace("mailto:", "").split("?")[0].strip()
        if "@" in email:
            emails.add(email)
            
    # Regex in text
    # Simple regex for email
    text = soup.get_text()
    found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    for e in found:
        # filter out common false positives or image files
        if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            emails.add(e)
            
    return list(emails)

def extract_phones(soup):
    phones = set()
    # Tel links
    for a in soup.select("a[href^='tel:']"):
        href = a.get("href", "")
        phone = href.replace("tel:", "").strip()
        if len(phone) > 6:
            phones.add(phone)
            
    # Regex is tricky for phones internationally/locally, 
    # relying mostly on tel links or specific patterns might be safer.
    # Let's try a generic one for Malaysia: +60... or 03-...
    text = soup.get_text()
    # +60 3-1234 5678 or 03-1234 5678
    matches = re.findall(r'(?:\+?60|0)[-\s]?[1-9][0-9]{0,2}[-\s]?[0-9]{3,4}[-\s]?[0-9]{3,4}', text)
    for m in matches:
        clean = clean_text(m)
        if len(clean) > 8:
            phones.add(clean)
            
    return list(phones)

def verify_url(url):
    if not url or url.lower() == 'nan': return None
    if not url.startswith('http'):
        return f"http://{url}"
    return url

def scan_website(session, start_url):
    contact_data = {
        "verified_emails": [],
        "verified_phones": [],
        "source_url": ""
    }
    
    try:
        print(f"  Visiting {start_url}...")
        resp = session.get(start_url, timeout=15, headers=HEADERS)
        
        # Checking for dead links
        if resp.status_code >= 400:
            print(f"  X Failed with status {resp.status_code}")
            return contact_data
            
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Extract from Home
        contact_data["verified_emails"].extend(extract_emails(soup))
        contact_data["verified_phones"].extend(extract_phones(soup))
        contact_data["source_url"] = start_url
        
        # If no email found, try to find a contact page
        if not contact_data["verified_emails"]:
            # Look for contact link
            contact_link = soup.find("a", href=True, string=re.compile(r"contact", re.I))
            if not contact_link:
                # Check href contains contact
                contact_link = soup.find("a", href=re.compile(r"contact", re.I))
                
            if contact_link:
                link = contact_link['href']
                full_link = urljoin(start_url, link)
                print(f"    -> Checking Contact Page: {full_link}")
                try:
                    c_resp = session.get(full_link, timeout=10, headers=HEADERS)
                    if c_resp.status_code == 200:
                        c_soup = BeautifulSoup(c_resp.text, "html.parser")
                        contact_data["verified_emails"].extend(extract_emails(c_soup))
                        contact_data["verified_phones"].extend(extract_phones(c_soup))
                        contact_data["source_url"] = full_link
                except Exception as e:
                    print(f"    -> Error parsing contact page: {e}")

    except Exception as e:
        print(f"  X Error: {e}")
        
    # Dedupe lists
    contact_data["verified_emails"] = list(set(contact_data["verified_emails"]))
    contact_data["verified_phones"] = list(set(contact_data["verified_phones"]))
    
    return contact_data

def main():
    if not INPUT_FILE.exists():
        print("Input file not found.")
        return
        
    session = requests.Session()
    
    with INPUT_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames + ["verified_emails", "verified_phones", "verification_source", "verification_status"]
        rows = list(reader)
        
    verified_rows = []
    
    print(f"Verifying {len(rows)} hotels...")
    
    for i, row in enumerate(rows, 1):
        name = row.get("name")
        website = row.get("website")
        print(f"[{i}/{len(rows)}] {name} ({website})")
        
        url = verify_url(website)
        
        if url:
            data = scan_website(session, url)
            
            emails = "; ".join(data["verified_emails"])
            phones = "; ".join(data["verified_phones"])
            source = data["source_url"]
            
            row["verified_emails"] = emails
            row["verified_phones"] = phones
            row["verification_source"] = source
            
            if emails or phones:
                row["verification_status"] = "Verified"
                print(f"  -> Found: {len(data['verified_emails'])} emails, {len(data['verified_phones'])} phones")
            else:
                row["verification_status"] = "No_Data_Found"
                print("  -> No contact info found on site.")
        else:
            row["verified_emails"] = ""
            row["verified_phones"] = ""
            row["verification_source"] = ""
            row["verification_status"] = "No_Website"
            print("  -> No valid website.")
            
        verified_rows.append(row)
        
    # Write output
    with OUTPUT_FILE.open("w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(verified_rows)
        
    print(f"\nVerification complete. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
