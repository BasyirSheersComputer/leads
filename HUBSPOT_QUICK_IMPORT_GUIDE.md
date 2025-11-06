# Hubspot Quick Import Guide

## ✅ YOUR FILE IS READY!

**File:** `Hubspot_Import_Ready_20251014_115453.csv`  
**Format:** Matches your existing Hubspot CRM structure  
**Records:** 334 contacts ready to import

---

## 🚀 Import in 5 Easy Steps

### Step 1: Go to Hubspot Contacts
- Log into your Hubspot account
- Navigate to **Contacts** > **Contacts**

### Step 2: Start Import
- Click the **Import** button (top right corner)
- Select **Import file from computer**

### Step 3: Upload File
- Click **Choose a file**
- Select: `Hubspot_Import_Ready_20251014_115453.csv`
- Click **Next**

### Step 4: Configure Import
- Select **One file**
- Select **One object: Contacts**
- Click **Next**

### Step 5: Review & Import
- Hubspot will **automatically map all columns** (they match your existing format!)
- Review the preview
- Choose duplicate handling:
  - **Recommended:** "Update existing records and create new ones" (uses Email as identifier)
- Click **Import**

---

## 📊 What's in the File

### Total Records: 334

**By Lifecycle Stage:**
- 🟢 **Customers:** 24 (existing ASTA customers)
- 🔵 **Leads:** 310 (new opportunities)

**By Contact Owner:**
- Joey: 184 contacts
- Mat: 77 contacts
- Others: 73 contacts distributed

**By Buying Role:**
- Decision Makers: 184 (CEOs, Directors, GMs, Managers)
- Technical Buyers: 5 (IT roles)
- Budget Holders: 5 (Procurement)
- Others: 140 (to be qualified)

**Contact Quality:**
- ✓ Has Email: 269 contacts (80.5%)
- ✓ Has Phone: 229 contacts (68.6%)

---

## 🎯 What's Been Mapped

Your consolidated data has been intelligently mapped to Hubspot format:

| Your Data | Hubspot Field | What's Included |
|-----------|---------------|-----------------|
| First Name + Last Name | First Name, Last Name | Cleaned and split |
| Names with titles | Salutation | Mr., Mrs., Ms., Dr., Prof., Datuk |
| Job Title | Job Title | Designation/position |
| Company | Company Name | Company or Hospital name |
| Person In Charge | Contact owner | Joey, Mat, Sugi, etc. |
| All event/product info | Notes | Comprehensive notes field |
| Lead Status + Industry | Lifecycle Stage | Lead or Customer |
| Job Title analysis | Buying Role | Decision Maker, Budget Holder, etc. |
| Email | Email | Email addresses |
| Phone Number | Mobile Phone Number | Phone/WhatsApp numbers |

---

## 📝 Notes Field Includes

Each contact's **Notes** field contains rich information:

```
SOURCE: Event name (Year) | INTERESTED IN: Products | CURRENT SYSTEM: PMS/HIS system | 
NEEDS: Problems/needs | REQUEST: Request type | BUSINESS: Business type | 
LOCATION: Country, City | NOTES: Comments | Lead captured: Timestamp
```

**Example:**
```
SOURCE: APHM 2025 (Jun 9-11) (2025) | INTERESTED IN: Mobile App | 
CURRENT SYSTEM: Origin, Quebee (standalone) | REQUEST: Meeting | 
BUSINESS: Hospital | LOCATION: Malaysia, Perak | ✓ Namecard collected | 
NOTES: Understand more. Appointment system, notification of appointment, 
show lab reports at mobile app | Lead captured: 2025-06-09 10:24:53
```

---

## 🔄 Lifecycle Stages Explained

**Customer** (24 records)
- Existing ASTA E-Invoice customers
- Ready for upsell opportunities

**Lead** (310 records)
- New leads from events
- Need initial contact and qualification

---

## 🎯 Buying Roles Auto-Assigned

Based on job title analysis:

**Decision Maker** (184)
- CEO, COO, CFO, Managing Director
- Director, General Manager
- Owner, President
- Department Heads

**Budget Holder** (5)
- Procurement roles
- Purchasing positions

**Technical Buyer** (5)
- IT Manager/Director
- Technology roles

---

## ⚡ After Import - Immediate Actions

### 1. Verify Import
- Check that all 334 contacts imported
- Review any skipped records (if any)
- Confirm contact owners are assigned

### 2. Create Lists
**High Priority List:**
- Filter: Notes contains "APHM 2025" (27 contacts - most recent!)
- Filter: Notes contains "Meeting" (high intent)

**By Event:**
- Filter by Notes contains "APHM", "Food & Hotel Malaysia", etc.

**By Geography:**
- Filter by Notes contains "Malaysia", "Singapore", "Vietnam"

### 3. Set Up Workflows

**Welcome Sequence:**
- Trigger: Contact created from import
- Condition: Lifecycle Stage = Lead
- Action: Enroll in welcome email sequence

**Meeting Request Follow-up:**
- Trigger: Notes contains "Meeting"
- Action: Create task for contact owner
- Priority: High

**Customer Upsell:**
- Trigger: Lifecycle Stage = Customer
- Action: Create task to review upsell opportunities

### 4. Create Tasks

For contact owners to follow up:
- Joey: 184 contacts
- Mat: 77 contacts
- Others: Distribute remaining

---

## 🎨 Hubspot Views to Create

### View 1: Hot Leads (2025 Events)
- Filter: Notes contains "2025"
- Sort: By Contact Owner
- Result: 27 APHM 2025 leads + 24 customers

### View 2: Meeting Requests
- Filter: Notes contains "Meeting"
- Sort: By Last Modified Date
- Priority: High

### View 3: Decision Makers
- Filter: Buying Role = "Decision Maker"
- Filter: Email is known
- Result: 184 key contacts

### View 4: Existing Customers
- Filter: Lifecycle Stage = "Customer"
- Result: 24 upsell opportunities

### View 5: By Geography
Create separate views for:
- Malaysia (159 contacts)
- Singapore (30 contacts)
- Vietnam (18 contacts)
- Thailand (~15 contacts)

---

## 🔍 Key Differences from Previous Format

### Old Format (Generic):
- 26 columns with many empty fields
- Separate columns for each data point
- Required extensive field mapping
- Not optimized for your Hubspot

### New Format (Hubspot-Optimized):
- ✅ 11 columns matching your exact Hubspot structure
- ✅ Consolidated rich data in Notes field
- ✅ Auto-maps on import (zero manual mapping!)
- ✅ Lifecycle Stages pre-assigned
- ✅ Buying Roles intelligently determined
- ✅ Contact Owners mapped from your team
- ✅ Salutations extracted from names
- ✅ Ready to use immediately after import

---

## 🎯 Priority Actions This Week

### Day 1: Import & Setup
1. ✅ Import the CSV file (5 minutes)
2. ✅ Create the 5 views listed above (10 minutes)
3. ✅ Set up basic workflows (15 minutes)

### Day 2-3: APHM 2025 Leads
1. Contact all 27 APHM 2025 leads (most recent!)
2. Update lifecycle stages as you qualify
3. Create deals for opportunities

### Day 4-5: Meeting Requests
1. Contact all leads with meeting requests
2. Schedule demos/presentations
3. Update buying roles as you learn more

### Week 2: Systematic Follow-up
1. Work through leads by owner
2. Focus on decision makers with email
3. Email campaigns for lower priority

---

## 📊 Expected Results

### Week 1:
- 334 contacts imported ✓
- 27 APHM 2025 leads contacted
- 5-10 meetings scheduled

### Month 1:
- 50+ leads qualified to opportunity
- 10+ proposals sent
- 3-5 deals closed

### Quarter 1:
- Full database engaged
- Pipeline of 100+ qualified opportunities
- Regular follow-up cadence established

---

## ❓ Troubleshooting

### If columns don't auto-map:
- Manually map each column to the corresponding Hubspot property
- The names match your existing template, so it should be straightforward

### If duplicates are created:
- Hubspot uses Email as the unique identifier
- Choose "Update existing" to prevent duplicates
- After import, use Hubspot's duplicate management tool

### If contact owner names don't match:
- Hubspot will leave them unassigned if names don't match exactly
- After import, manually assign or update the mapping
- Common mappings:
  - "Joey" → Your Joey's Hubspot user
  - "Mat" → Your Mat's Hubspot user

### If some records are skipped:
- Check for missing required fields (Email is recommended but not required)
- Review skipped records report
- Can manually add or re-import with fixes

---

## 🎉 Success Indicators

After successful import, you should see:

✓ **334 contacts** in your Hubspot  
✓ **24 marked as Customers** (existing clients)  
✓ **310 marked as Leads** (new opportunities)  
✓ **Contacts assigned** to Joey, Mat, and team  
✓ **Rich Notes** with event and product information  
✓ **Buying Roles** assigned to 194 contacts  
✓ **Ready to filter**, segment, and follow up  

---

## 🏁 You're All Set!

Your file is:
- ✅ Formatted to match your Hubspot exactly
- ✅ Optimized for easy import
- ✅ Enriched with intelligent categorization
- ✅ Ready to drive sales results

**Just upload and start converting! 🚀**

---

*File generated: October 14, 2025*  
*Format validated against: hubspot-crm-exports-all-contacts-2025-10-13.csv*  
*334 contacts ready for import*


