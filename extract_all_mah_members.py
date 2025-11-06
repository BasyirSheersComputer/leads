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
                        
                        members.set(membershipNumber, {
                            name: memberName,
                            membershipNumber: membershipNumber,
                            starRating: starRating,
                            roomCount: roomCount,
                            state: state,
                            category: category,
                            address: address,
                            phone: phone,
                            email: email,
                            website: website
                        });
                    }
                }
            });
            
            return Array.from(members.values());
        }
    """)

def main():
    all_members = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to the first page
            page.goto('https://www.hotels.org.my/members')
            page.wait_for_load_state('networkidle')
            
            # Extract from all 40 pages
            for page_num in range(1, 41):
                print(f"Extracting page {page_num}...")
                
                # Extract members from current page
                members = extract_members_from_page(page)
                all_members.extend(members)
                print(f"Found {len(members)} members on page {page_num}")
                
                # Navigate to next page if not the last page
                if page_num < 40:
                    try:
                        # Select next page from dropdown
                        page.select_option('#body_uc_page_ddl', str(page_num + 1))
                        page.wait_for_load_state('networkidle')
                        time.sleep(2)  # Wait for page to load
                    except Exception as e:
                        print(f"Error navigating to page {page_num + 1}: {e}")
                        break
            
            # Remove duplicates based on membership number
            unique_members = {}
            for member in all_members:
                unique_members[member['membershipNumber']] = member
            
            final_members = list(unique_members.values())
            print(f"Total unique members extracted: {len(final_members)}")
            
            # Save to CSV
            with open('MAH_Members_Complete_2025.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'membershipNumber', 'starRating', 'roomCount', 'state', 'category', 'address', 'phone', 'email', 'website']
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
