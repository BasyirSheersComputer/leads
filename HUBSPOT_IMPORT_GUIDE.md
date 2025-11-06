# Hubspot Import Guide for Consolidated Leads

## Overview
This guide will help you import your consolidated leads database into Hubspot CRM.

**Total Leads:** 334
- Hospital Leads: 85
- Hospitality Leads: 225
- Existing Customers: 24

---

## Files Generated

### 1. **Consolidated_Leads_CRM_*_ENHANCED.xlsx**
- Main CRM database with professional formatting
- Multiple sheets for different categories
- Dropdown validations for easy data entry
- Perfect for internal lead management

### 2. **Consolidated_Leads_Hubspot_Import_*.csv**
- CSV file optimized for Hubspot import
- Contains all 334 leads with standardized fields
- Ready to upload directly to Hubspot

---

## Field Mapping for Hubspot

The CSV file includes the following fields that map to Hubspot properties:

| Excel Column | Hubspot Property | Type | Description |
|--------------|------------------|------|-------------|
| Lead ID | Custom Property | Text | Unique identifier (LEAD-0001, etc.) |
| First Name | First Name | Text | Contact's first name |
| Last Name | Last Name | Text | Contact's last name |
| Email | Email | Email | Primary email address |
| Phone Number | Phone Number | Phone | Contact phone number |
| Job Title | Job Title | Text | Position/designation |
| Company | Company Name | Text | Organization name |
| Industry | Industry | Dropdown | Hospital, Hospitality, or Existing Customer |
| Type of Business | Custom Property | Text | Specific business type (Hotel, Restaurant, etc.) |
| Country | Country | Text | Country of operation |
| Location | City/State | Text | Specific location or address |
| Lead Source | Original Source | Dropdown | Event name |
| Event Year | Custom Property | Text | Year of event |
| Lead Status | Lead Status | Dropdown | Current status of lead |
| Interested Products | Custom Property | Text | Products/solutions of interest |
| Current System | Custom Property | Text | Existing PMS/POS/HIS system |
| Problems/Needs | Custom Property | Text | Customer pain points |
| Request Type | Custom Property | Text | Type of inquiry |
| Comments | Notes | Text | Additional comments and context |
| Person In Charge | Owner | User | Your team member assigned |
| Has Namecard | Custom Property | Text | Whether namecard was collected |
| Original Timestamp | Create Date | Date | When lead was captured |

---

## Step-by-Step Hubspot Import

### Step 1: Prepare Custom Properties in Hubspot

Before importing, create these custom properties in Hubspot:

1. Go to **Settings** > **Properties** > **Contact Properties**
2. Click **Create Property** and add the following:

| Property Name | Field Type | Description |
|---------------|------------|-------------|
| lead_id | Single-line text | Unique Lead Identifier |
| event_year | Single-line text | Event Year |
| type_of_business | Single-line text | Specific Business Type |
| interested_products | Multiple-line text | Products/Solutions of Interest |
| current_system | Single-line text | Current System (PMS/POS/HIS) |
| problems_needs | Multiple-line text | Problems and Needs |
| request_type | Single-line text | Request Type |
| has_namecard | Dropdown | Yes/No |

### Step 2: Import the CSV File

1. **Go to Hubspot Contacts**
   - Navigate to Contacts > Contacts in Hubspot

2. **Start Import**
   - Click **Import** button (top right)
   - Select **Import file from computer**

3. **Choose File**
   - Select `Consolidated_Leads_Hubspot_Import_*.csv`
   - Choose **One file**
   - Select **One object: Contacts**

4. **Map Columns**
   - Hubspot will automatically try to map columns
   - Review and adjust mappings:
     - Map "Lead ID" to your custom `lead_id` property
     - Map "Event Year" to your custom `event_year` property
     - Map "Type of Business" to `type_of_business`
     - Map "Interested Products" to `interested_products`
     - Map "Current System" to `current_system`
     - Map "Problems/Needs" to `problems_needs`
     - Map "Request Type" to `request_type`
     - Map "Has Namecard" to `has_namecard`
     - Map standard fields (Name, Email, Phone, Company, etc.)

5. **Set Owner**
   - Map "Person In Charge" to "Contact Owner"
   - You may need to create user mappings:
     - J → Joey
     - M → Mat
     - etc.

6. **Import Settings**
   - Choose how to handle duplicates:
     - **Recommended:** Update existing records and create new ones
   - This prevents duplicate contacts

7. **Review and Import**
   - Review the summary
   - Click **Import** to start the process

### Step 3: Verify Import

1. Check the import status in Hubspot
2. Review a sample of imported contacts
3. Verify custom fields are populated correctly
4. Check that owners are assigned properly

---

## Post-Import Actions

### 1. Create Lists for Segmentation

Create smart lists to organize your leads:

**By Industry:**
- Hospital Leads (Industry = "Hospital")
- Hospitality Leads (Industry = "Hospitality")
- Existing Customers (Industry = "Existing Customer")

**By Status:**
- New Leads (Lead Status = "New")
- Requires Follow-up (Last Contact Date < 30 days ago)
- Hot Leads (Request Type contains "Meeting")

**By Event:**
- APHM 2025 (Lead Source = "APHM 2025")
- Recent Events (Event Year = "2025")

### 2. Set Up Workflows

Create automated workflows for:

**Welcome Email Sequence:**
- Trigger: Contact created from import
- Action: Send welcome email based on Industry
- Delay: 2 days
- Action: Assign task to owner for follow-up

**Follow-up Reminders:**
- Trigger: Lead Status = "Contacted"
- Delay: 7 days
- Action: Create task for owner to follow up

**Lead Nurturing:**
- Trigger: Interested Products contains specific items
- Action: Enroll in product-specific email sequence

### 3. Create Custom Reports

Build reports to track:
- Leads by Source (Event)
- Conversion Rate by Industry
- Leads by Owner
- Follow-up Activity
- Interested Products Distribution

### 4. Set Up Deal Pipeline

For qualified leads, create deals:
1. Go to Sales > Deals
2. Create deal stages:
   - Prospect
   - Demo Scheduled
   - Proposal Sent
   - Negotiation
   - Closed Won
   - Closed Lost

---

## Best Practices

### Immediate Actions (First Week)

1. **Prioritize 2025 Leads**
   - Filter for Event Year = "2025"
   - These are the freshest leads (APHM 2025 - 27 leads)

2. **Contact Leads Requesting Meetings**
   - Filter Request Type contains "Meeting"
   - These leads have high intent

3. **Follow up with Namecard Holders**
   - Filter Has Namecard = "Yes"
   - These leads showed strong interest

### Ongoing Management

1. **Update Lead Status** after each interaction
2. **Log Notes** on every contact attempt
3. **Schedule Follow-ups** using Tasks
4. **Create Deals** for qualified opportunities
5. **Track Email Opens** in sequences to gauge interest

### Team Coordination

**Assign by Person In Charge:**
- Joey: 138 leads
- J/Joey combined: ~176 leads
- Mat: 33 leads
- M: 29 leads
- Others: Distribute remaining leads

---

## Data Quality Tips

### Keep Data Clean

1. **Standardize Phone Numbers**
   - Use Hubspot's phone format automation
   - Add country codes where missing

2. **Validate Email Addresses**
   - Use Hubspot's email validation
   - Remove bounced emails

3. **Update Company Information**
   - Enrich company data using Hubspot Insights
   - Add company websites where available

4. **Merge Duplicates**
   - Run duplicate detection weekly
   - Merge duplicates to maintain clean database

---

## Troubleshooting

### Common Import Issues

**Issue: Columns Not Mapping**
- Solution: Ensure custom properties are created before import
- Check spelling and field types match

**Issue: Duplicates Created**
- Solution: Use email as unique identifier
- Choose "Update existing" option during import

**Issue: Owner Not Assigned**
- Solution: Create user mapping file
- Map "Person In Charge" values to Hubspot users

**Issue: Dates Not Importing**
- Solution: Ensure date format is YYYY-MM-DD HH:MM:SS
- Convert in Excel before export if needed

---

## Integration with Other Tools

### Connect with:

1. **Email (Gmail/Outlook)**
   - Connect your email to log conversations automatically

2. **Calendar**
   - Sync meetings and follow-ups

3. **WhatsApp/Phone**
   - Use Hubspot mobile app to log calls
   - Many leads have WhatsApp numbers - use for quick contact

4. **Marketing Tools**
   - Mailchimp or Hubspot Marketing Hub
   - Create targeted campaigns by product interest

---

## Key Metrics to Track

1. **Lead Response Rate**
   - % of leads contacted within 48 hours
   - Target: 80%+

2. **Conversion Rate**
   - % of leads that become customers
   - Track by source/event

3. **Average Deal Value**
   - By product category
   - By industry segment

4. **Sales Cycle Length**
   - Hospital vs Hospitality comparison
   - Event follow-up effectiveness

5. **Lead Source ROI**
   - Which events generate best leads
   - Plan future event participation

---

## Contact Information by Category

### Hospital Leads (85 total)
- **Main Events:** 
  - APHM 2025: 27 leads (Most recent!)
  - APHM 2023: 38 leads
  - APHM 2024: 20 leads
- **Products of Interest:** Mobile Apps, Queue Systems, Design Kiosks
- **Decision Makers:** IT Managers, Nursing Officers, Hospital Administrators

### Hospitality Leads (225 total)
- **Main Events:**
  - FHA HoReCa: 61 leads
  - Food & Hotel Malaysia 2023: 52 leads
  - Food & Hotel Indonesia 2023: 39 leads
- **Products of Interest:** Hotel Kiosks, PMS Integration, Mobile Ordering
- **Decision Makers:** General Managers, IT Directors, Operations Managers

### Existing Customers (24 records)
- **Source:** ASTA E-Invoice Registration
- **Status:** Active customers
- **Opportunity:** Upsell additional products/services

---

## Support

For questions or issues with the import:
1. Review Hubspot's import documentation
2. Check field mappings in Hubspot settings
3. Contact Hubspot support for technical issues

---

**Generated:** October 14, 2025
**Total Records:** 334 leads
**Ready for:** Immediate import and follow-up

Good luck with your lead management! 🚀


