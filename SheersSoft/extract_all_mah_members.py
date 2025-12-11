#!/usr/bin/env python3
"""
Comprehensive MAH Members Extraction Script
This script will extract all members from all pages of the MAH directory
"""

import csv
import time
import json
from playwright.sync_api import sync_playwright

def extract_members_from_page(page):
    """Extract members from current page"""
    return page.evaluate("""
        () => {
            const members = new Map();
            const memberElements = document.querySelectorAll('h3');
            
            memberElements.forEach(heading => {
                if (heading.textContent.includes('(') && heading.textContent.includes(')')) {
                    const memberName = heading.textContent.split(' (')[0];
                    const membershipNumber = heading.textContent.match(/\\((\\d+)\\)/)?.[1] || '';
                    
                    // Skip if already processed
                    if (members.has(membershipNumber)) return;
                    
                    // Get the parent container
                    const container = heading.closest('div');
                    if (container) {
                        // Extract location and star rating
                        const locationLink = container.querySelector('a[href*="views"]');
                        const locationText = locationLink ? locationLink.textContent : '';
                        
                        // Extract address
                        const addressP = container.querySelector('p');
                        let address = '';
                        if (addressP) {
                            const addressParts = [];
                            addressP.childNodes.forEach(node => {
                                if (node.nodeType === Node.TEXT_NODE) {
                                    addressParts.push(node.textContent.trim());
                                }
                            });
                            address = addressParts.join(', ');
                        }
                        
                        // Extract contact info
                        const contactList = container.querySelector('ul');
                        let phone = '';
                        let email = '';
                        let website = '';
                        
                        if (contactList) {
                            const listItems = contactList.querySelectorAll('li');
                            listItems.forEach(li => {
                                const text = li.textContent.trim();
                                if (text.includes('@')) {
                                    email = text;
                                } else if (text.startsWith('http') || text.startsWith('www')) {
                                    website = text;
                                } else if (text.match(/[\\d\\s\\-\\+\\(\\)]+/) && text.length > 5 && !text.includes('Star') && !text.includes('rooms') && !text.includes('Associate')) {
                                    phone = text;
                                }
                            });
                        }
                        
                        // Parse location and star rating
                        let state = '';
                        let starRating = '';
                        let roomCount = '';
                        let category = 'Others';
                        
                        if (locationText) {
                            const parts = locationText.split(', ');
                            if (parts.length >= 2) {
                                state = parts[0];
                                const secondPart = parts[1];
                                if (secondPart.includes('Star')) {
                                    starRating = secondPart.split(' ')[0] + ' ' + secondPart.split(' ')[1];
                                    const roomMatch = secondPart.match(/\\((\\d+) rooms\\)/);
                                    roomCount = roomMatch ? roomMatch[1] : '';
                                } else if (secondPart.includes('Associate')) {
                                    starRating = 'Associate';
                                    category = 'Associate';
                                } else if (secondPart.includes('Orchid')) {
                                    starRating = 'Orchid';
                                    const roomMatch = secondPart.match(/\\((\\d+) rooms\\)/);
                                    roomCount = roomMatch ? roomMatch[1] : '';
                                } else {
                                    starRating = 'Others';
                                    const roomMatch = secondPart.match(/\\((\\d+) rooms\\)/);
                                    roomCount = roomMatch ? roomMatch[1] : '';
                                }
                            }
                        }
                        
                            website: website
                        };
                        
                        // Generate unique ID in JS
                        obj.unique_id = membershipNumber ? `MAH-${membershipNumber}` : `MAH-NOID-${memberName.substring(0,5)}`;
                        
                        // Normalize category/starRating mismatch
                        // The segmenter expects 'category' to contain '5 Star' etc.
                        // In this script, starRating holds that info.
                        // So we will overwrite category with starRating if starRating is descriptive
                        if (starRating && starRating !== 'Others') {
                             obj.category = starRating;
                        } else if (!obj.category) {
                             obj.category = 'Others';
                        }

                        // Map to expected output keys
                        obj.rooms = roomCount;
                        obj.membership_number = membershipNumber;
                        
                        members.set(membershipNumber, obj);
                    }
                }
            });
            
            // Transform values to match schema
            return Array.from(members.values()).map(m => ({
                unique_id: m.unique_id,
                name: m.name,
                membership_number: m.membership_number,
                state: m.state,
                category: m.category, // Use the normalized category
                rooms: m.rooms,
                address: m.address,
                phone: m.phone,
                email: m.email,
                website: m.website
            }));
        }
    """)

def main():
    all_members = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to the first page
            page.goto('https://www.hotels.org.my/members')
            page.wait_for_load_state('networkidle')
            
            # Get total pages from dropdown
            try:
                # Wait for dropdown to be visible
                page.wait_for_selector('#body_uc_page_ddl', state='attached')
                
                # Get all option values
                options = page.eval_on_selector_all('#body_uc_page_ddl option', 'options => options.map(o => o.value)')
                # Filter out non-numeric if any, though usually they are "1", "2"...
                valid_pages = [int(x) for x in options if x.isdigit()]
                
                if valid_pages:
                    max_page = max(valid_pages)
                else:
                    max_page = 40  # Fallback
                    
                print(f"Detected {max_page} pages.")
            except Exception as e:
                print(f"Could not detect total pages, defaulting to 40. Error: {e}")
                max_page = 40

            # Extract from all pages
            for page_num in range(1, max_page + 1):
                print(f"Extracting page {page_num} of {max_page}...")
                
                # Extract members from current page
                members = extract_members_from_page(page)
                all_members.extend(members)
                print(f"Found {len(members)} members on page {page_num}")
                
                # Navigate to next page if not the last page
                if page_num < max_page:
                    try:
                        # Select next page from dropdown
                        next_page_str = str(page_num + 1)
                        page.select_option('#body_uc_page_ddl', next_page_str)
                        
                        # Wait for the page content to update - relying on networkidle might be enough but let's be safe
                        # We can wait for a specific element that signals change, or just wait for load state
                        page.wait_for_load_state('networkidle')
                        time.sleep(3)  # Explicit wait to be polite and ensure rendering
                        
                    except Exception as e:
                        print(f"Error navigating to page {page_num + 1}: {e}")
                        # Try to recover or break?
                        # If we can't navigate, we might be stuck.
                        # Attempting to reload or continue might be futile without complex logic.
                        print("Stopping extraction due to navigation error.")
                        break
            
            # Remove duplicates based on unique_id or membership_number
            unique_members = {}
            for member in all_members:
                unique_members[member['membership_number']] = member
            
            final_members = list(unique_members.values())
            print(f"Total unique members extracted: {len(final_members)}")
            
            # Save to CSV
            with open('MAH_Members_Complete_2025.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['unique_id', 'name', 'membership_number', 'state', 'category', 'rooms', 'address', 'phone', 'email', 'website']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(final_members)
            
            print("Data saved to MAH_Members_Complete_2025.csv")
            
        except Exception as e:
            print(f"Error during extraction: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
