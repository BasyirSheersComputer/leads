# Origin Studios Leads - CSV Structure

## Updated: November 3, 2025

### File: `originistudios_leads.csv`

---

## Column Structure (10 Columns)

| # | Column Name | Data Type | Example | Description |
|---|-------------|-----------|---------|-------------|
| 1 | **No.** | Integer | 1, 2, 3... | Sequential lead number |
| 2 | **Company Name** | Text | Beacon Hospital | Official organization name |
| 3 | **Type** | Text | Hospital/Medical Center | Facility type category |
| 4 | **Industry** | Text | Healthcare | Industry sector |
| 5 | **Estimated Location** | Text | Kuala Lumpur, Malaysia | Geographic location |
| 6 | **Phone** | Text | +603-7653 1000 | Contact phone number (international format) |
| 7 | **Email** | Email | info@beaconhospital.com.my | Contact email address |
| 8 | **Website** | URL | beaconhospital.com.my | Company website |
| 9 | **Source** | Text | originistudios.com (Client List) | Lead source |
| 10 | **Notes** | Text | Origin Studios customer... | Additional information |

---

## Sample Data

### Example Row 1:
```
No.: 1
Company Name: Alhaya Fertility Centre
Type: Fertility/IVF Center
Industry: Healthcare
Estimated Location: Malaysia
Phone: +603-7931 6888
Email: info@alhaya.com.my
Website: alhaya.com.my
Source: originistudios.com (Client List)
Notes: Origin Studios customer - likely uses digital healthcare solutions
```

### Example Row 2:
```
No.: 10
Company Name: Beacon Hospital
Type: Hospital/Medical Center
Industry: Healthcare
Estimated Location: Kuala Lumpur/Selangor, Malaysia
Phone: +603-7653 1000
Email: info@beaconhospital.com.my
Website: beaconhospital.com.my
Source: originistudios.com (Client List)
Notes: Origin Studios customer - likely uses digital healthcare solutions
```

### Example Row 3:
```
No.: 25
Company Name: Mandaya Hospital Kerawang
Type: Hospital/Medical Center
Industry: Healthcare
Estimated Location: West Java, Indonesia
Phone: +62 267 641 2525
Email: info@mandayahospital.com
Website: mandayahospital.com
Source: originistudios.com (Client List)
Notes: Origin Studios customer - likely uses digital healthcare solutions
```

---

## Data Quality Metrics

- **Total Records**: 55
- **Phone Number Coverage**: 100% (55/55)
- **Email Address Coverage**: 100% (55/55)
- **Website Coverage**: 100% (55/55)
- **Complete Contact Info**: 100% (55/55)

---

## Phone Number Format

All phone numbers follow international format:
- **Malaysia**: `+60X-XXXX XXXX` (e.g., +603-7653 1000)
- **Indonesia**: `+62 XXX XXXX XXXX` (e.g., +62 21 2982 9999)

---

## Email Format Patterns

Common email patterns found:
- `info@domain.com` (general inquiries)
- `enquiry@domain.com` (customer service)
- `contact@domain.com` (general contact)
- Department-specific: `aiss@assunta.com.my`, `boc.klang@beaconhospital.com.my`

---

## Import Instructions

### For CRM Systems (HubSpot, Salesforce, etc.):

1. **Field Mapping**:
   - Company Name → Company/Account Name
   - Phone → Primary Phone
   - Email → Primary Email
   - Website → Company Website
   - Type → Industry/Category
   - Estimated Location → Company Location
   - Source → Lead Source
   - Notes → Description/Notes

2. **Data Validation**:
   - All phone numbers are in international format
   - All emails are properly formatted
   - No duplicate companies

3. **Recommended Tags**:
   - `Origin Studios Client`
   - `Healthcare Provider`
   - Geographic tags (Malaysia, Indonesia, etc.)

### For Email Marketing (Mailchimp, SendGrid, etc.):

1. **Required Fields**:
   - Email (Column 7)
   - Company Name (Column 2)
   - Phone (Column 6)

2. **Segmentation Options**:
   - By Type (Fertility, Oncology, General Hospital, etc.)
   - By Location (Malaysia vs Indonesia, by state/city)
   - By Organization Size (implied by facility type)

3. **Personalization Fields**:
   - Company_Name
   - Facility_Type
   - Location

---

## File Compatibility

- **Format**: CSV (Comma-Separated Values)
- **Encoding**: UTF-8
- **Line Endings**: Windows (CRLF)
- **Delimiter**: Comma (,)
- **Text Qualifier**: Double quotes (") for fields containing commas

---

## Change Log

### November 3, 2025
- ✅ Separated Email into dedicated column (was embedded in Notes)
- ✅ Renamed 'Contact' column to 'Phone' for clarity
- ✅ Reorganized columns in logical order
- ✅ Cleaned up Notes field (removed embedded contact info)
- ✅ Verified all 55 records updated successfully

### November 3, 2025 (Initial)
- ✅ Created initial CSV with 55 leads
- ✅ Added contact information for all organizations
- ✅ Categorized by facility type
- ✅ Added geographic locations

---

## Usage Notes

- **Ready for Import**: File is immediately usable in any CRM or email marketing platform
- **No Duplicates**: All 55 organizations are unique
- **Verified Contacts**: All contact information sourced from public records and official websites
- **GDPR/Privacy**: All data is publicly available business contact information
- **Update Frequency**: Recommended to verify contact information quarterly

---

**Last Updated**: November 3, 2025  
**File Version**: 2.0  
**Contact Coverage**: 100%


