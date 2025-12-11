import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import sys

OUTPUT_FILE = "MAH_Members_Complete_2025.csv"

def clean_text(text):
    if not text: return ""
    return " ".join(text.strip().split())

def extract_members(soup):
    members = []
    blocks = soup.select(".sp-blog-block")
    for block in blocks:
        try:
            name_tag = block.find("h3", class_="entry-title")
            if not name_tag: continue
            
            full_title = clean_text(name_tag.get_text())
            # Parse Name (Membership)
            # e.g. "@THOME BOUTIQUE HOTEL (1229)"
            match = re.match(r"(.*?)\s*\((\d+)\)$", full_title)
            if match:
                name = match.group(1)
                membership_number = match.group(2)
            else:
                name = full_title
                membership_number = ""

            # Check dupes? We'll handle unique dict later.

            # Meta info: State, Category/Star, Rooms
            # <div class="sp-blog-meta"> ... <li>... Sarawak, Others (96 rooms) ...
            meta_tag = block.select_one(".sp-blog-meta li a")
            meta_text = clean_text(meta_tag.get_text()) if meta_tag else ""
            
            state = ""
            category = "Others" # fallback
            rooms = ""
            
            # Parse meta text
            # e.g. "Kuala Lumpur, 4 Star (364 rooms)"
            # e.g. "Selangor, Associate"
            
            if meta_text:
                parts = [p.strip() for p in meta_text.split(',')]
                if len(parts) >= 1:
                    state = parts[0]
                if len(parts) >= 2:
                    remainder = ", ".join(parts[1:])
                    # Check for rooms
                    rooms_match = re.search(r"\((\d+)\s+rooms?\)", remainder)
                    rooms = rooms_match.group(1) if rooms_match else ""
                    
                    # Category/Star
                    # Remove room part
                    cat_part = re.sub(r"\(\d+\s+rooms?\)", "", remainder).strip()
                    if cat_part:
                        category = cat_part
            
            # Address
            address_p = block.find("p", id=lambda x: x and x.startswith("body_rpt_p_address"))
            address = ""
            if address_p:
                # Replace br with newline or comma
                for br in address_p.find_all("br"):
                    br.replace_with(", ")
                address = clean_text(address_p.get_text())

            # Contact
            phone = ""
            email = ""
            website = ""
            
            contacts = block.select(".sp-contacts-list li")
            for li in contacts:
                txt = clean_text(li.get_text())
                if "@" in txt:
                    email = txt
                elif txt.lower().startswith("http") or txt.lower().startswith("www"):
                    website = txt
                elif any(c.isdigit() for c in txt) and len(txt) > 5:
                    phone = txt
            
            # Generate unique_id
            unique_id = f"MAH-{membership_number}" if membership_number else f"MAH-NOID-{name[:10].replace(' ','')}"

            members.append({
                "unique_id": unique_id,
                "name": name,
                "membership_number": membership_number,
                "state": state,
                "category": category,
                "rooms": rooms,
                "address": address,
                "phone": phone,
                "email": email,
                "website": website
            })
            
        except Exception as e:
            print(f"Error extracting member: {e}")
            continue
            
    return members

def main():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })
    
    url = "https://hotels.org.my/members"
    print(f"Fetching page 1 from {url}...")
    
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch initial page: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    
    all_members = []
    
    # Extract page 1
    page1_members = extract_members(soup)
    all_members.extend(page1_members)
    print(f"Page 1: Found {len(page1_members)} members.")
    
    # Determine total pages?
    # The select has options.
    select = soup.select_one("select#body_uc_page_ddl")
    if not select:
        print("Pagination dropdown not found. Assuming single page or error.")
        max_pages = 1
    else:
        options = select.find_all("option")
        # values are 0, 1, 2...
        # max value + 1 = total pages
        values = [int(o['value']) for o in options if o['value'].isdigit()]
        max_pages = max(values) + 1 if values else 1
        print(f"Detected {max_pages} pages.")

    # Loop for remaining pages
    # We are already on page 1 (index 0).
    # We need to fetch index 1 to max_pages-1
    
    # We need current ViewState
    viewstate = soup.select_one("#__VIEWSTATE")['value']
    viewstategen = soup.select_one("#__VIEWSTATEGENERATOR")['value']
    eventvalidation = soup.select_one("#__EVENTVALIDATION")['value']
    
    for page_idx in range(1, max_pages):
        print(f"Fetching page {page_idx + 1}/{max_pages}...")
        
        payload = {
            "__EVENTTARGET": "ctl00$body$uc_page$ddl",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstategen,
            "__EVENTVALIDATION": eventvalidation,
            "ctl00$body$txt_search": "", # Search box
            "ctl00$body$ddl_rating": "00000000-0000-0000-0000-000000000000",
            "ctl00$body$ddl_state": "00000000-0000-0000-0000-000000000000",
            "ctl00$body$ddl_category": "00000000-0000-0000-0000-000000000000",
            "ctl00$body$uc_page$ddl": str(page_idx)
        }
        
        try:
            resp = session.post(url, data=payload, timeout=30)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Extract
            page_mems = extract_members(soup)
            all_members.extend(page_mems)
            print(f"Found {len(page_mems)} members.")
            
            # Update ViewState for next loop
            vs_tag = soup.select_one("#__VIEWSTATE")
            vg_tag = soup.select_one("#__VIEWSTATEGENERATOR")
            ev_tag = soup.select_one("#__EVENTVALIDATION")
            
            if vs_tag: viewstate = vs_tag['value']
            if vg_tag: viewstategen = vg_tag['value']
            if ev_tag: eventvalidation = ev_tag['value']
            
            time.sleep(1) # Be polite
            
        except Exception as e:
            print(f"Error fetching page {page_idx + 1}: {e}")
            # Try to continue? If viewstate is lost, we might need to break
            # But maybe next request can use old viewstate? Unlikely.
            print("Stopping pagination.")
            break
            
    # Deduplicate
    unique_map = {}
    for m in all_members:
        unique_map[m['unique_id']] = m
        
    final_list = list(unique_map.values())
    print(f"Total unique members: {len(final_list)}")
    
    # Save CSV
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['unique_id', 'name', 'membership_number', 'state', 'category', 'rooms', 'address', 'phone', 'email', 'website']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_list)
        
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
