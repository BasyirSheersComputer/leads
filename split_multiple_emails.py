import pandas as pd
import re
import os
from datetime import datetime

class MultipleEmailSplitter:
    """Split entries with multiple emails into separate rows"""
    
    def __init__(self):
        self.email_pattern = re.compile(
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        )
        self.stats = {
            'files_processed': 0,
            'rows_split': 0,
            'new_rows_created': 0
        }
    
    def extract_emails(self, text):
        """Extract all valid emails from text"""
        if pd.isna(text) or text == '':
            return []
        
        text_str = str(text)
        
        # Find all email addresses using regex
        emails = self.email_pattern.findall(text_str)
        
        # Clean and deduplicate
        cleaned_emails = []
        for email in emails:
            email_clean = email.strip().lower()
            if email_clean and email_clean not in cleaned_emails:
                cleaned_emails.append(email_clean)
        
        return cleaned_emails
    
    def process_file(self, filepath):
        """Process a file and split multiple emails"""
        print(f"\nProcessing: {filepath}")
        
        try:
            # Read file
            ext = os.path.splitext(filepath)[1].lower()
            
            if ext == '.csv':
                df = pd.read_csv(filepath, encoding='utf-8')
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath)
            else:
                print(f"  ⚠️  Unsupported file type: {ext}")
                return None
            
            # Find email columns
            email_columns = []
            for col in df.columns:
                col_lower = str(col).lower()
                if 'email' in col_lower or 'e-mail' in col_lower or 'mail' in col_lower:
                    email_columns.append(col)
            
            if not email_columns:
                print(f"  ℹ️  No email columns found")
                return None
            
            email_col = email_columns[0]  # Use first email column
            print(f"  📧 Processing column: {email_col}")
            
            # Find rows with multiple emails
            new_rows = []
            rows_to_drop = []
            
            for idx, row in df.iterrows():
                email_value = row[email_col]
                emails = self.extract_emails(email_value)
                
                if len(emails) > 1:
                    print(f"  🔀 Row {idx + 2}: Found {len(emails)} emails")
                    
                    # Create a new row for each email
                    for i, email in enumerate(emails):
                        new_row = row.copy()
                        new_row[email_col] = email
                        
                        # Add suffix to name/company if it exists to differentiate
                        if 'First Name' in df.columns and pd.notna(new_row['First Name']):
                            if i > 0:  # Don't modify first one
                                new_row['First Name'] = f"{new_row['First Name']} (Contact {i+1})"
                        
                        new_rows.append(new_row)
                    
                    rows_to_drop.append(idx)
                    self.stats['rows_split'] += 1
                    self.stats['new_rows_created'] += len(emails)
            
            if not new_rows:
                print(f"  ✓ No multiple-email entries found")
                return None
            
            # Remove original rows with multiple emails
            df_cleaned = df.drop(rows_to_drop)
            
            # Add new split rows
            df_new_rows = pd.DataFrame(new_rows)
            df_final = pd.concat([df_cleaned, df_new_rows], ignore_index=True)
            
            # Sort by the email column
            df_final = df_final.sort_values(by=email_col)
            
            print(f"  ✅ Split {len(rows_to_drop)} rows into {len(new_rows)} rows")
            print(f"  📊 Original rows: {len(df)}, Final rows: {len(df_final)}")
            
            return df_final
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            return None
    
    def save_file(self, df, original_path):
        """Save the split file"""
        try:
            # Create output directory
            output_dir = "split_emails"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output filename
            base_name = os.path.basename(original_path)
            name_without_ext = os.path.splitext(base_name)[0]
            ext = os.path.splitext(base_name)[1].lower()
            
            # Remove existing CLEANED timestamp if present
            name_without_ext = re.sub(r'_CLEANED_\d{8}_\d{6}', '', name_without_ext)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{name_without_ext}_SPLIT_EMAILS_{timestamp}{ext}"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save based on file type
            if ext == '.csv':
                df.to_csv(output_path, index=False, encoding='utf-8')
            elif ext in ['.xlsx', '.xls']:
                df.to_excel(output_path, index=False, engine='openpyxl')
            
            print(f"  💾 Saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"  ❌ Error saving: {str(e)}")
            return None

def main():
    """Main execution"""
    print("="*80)
    print("MULTIPLE EMAIL SPLITTER")
    print("="*80)
    print("\nThis tool will split rows with multiple emails into separate rows.")
    print("Recommended for files where you want to contact each email separately.\n")
    
    splitter = MultipleEmailSplitter()
    
    # Process cleaned files
    cleaned_dir = "cleaned_leads"
    
    if not os.path.exists(cleaned_dir):
        print(f"❌ Directory not found: {cleaned_dir}")
        print("Please run verify_and_clean_emails.py first!")
        return
    
    files_to_process = [
        # Process the main import files that had multiple email issues
        os.path.join(cleaned_dir, "Hubspot_Import_FINAL_20251016_CLEANED_20251106_152314.csv"),
        os.path.join(cleaned_dir, "Priority_Contact_List_CLEANED_20251106_152315.csv"),
        os.path.join(cleaned_dir, "Leads - FHM 2025_FINAL_20251016_CLEANED_20251106_152318.xlsx"),
        os.path.join(cleaned_dir, "Leads - FHM 2025_CLEANED_20251106_152321.xlsx"),
        os.path.join(cleaned_dir, "FHA HoReCa Questionnaire (Responses)_CLEANED_20251106_152316.xlsx"),
        os.path.join(cleaned_dir, "FHMB2024 (Responses)_CLEANED_20251106_152316.xlsx"),
        os.path.join(cleaned_dir, "Questionnaire_ Food & Hotel Malaysia 2023 (Responses)_CLEANED_20251106_152317.xlsx"),
    ]
    
    for filepath in files_to_process:
        if not os.path.exists(filepath):
            print(f"\n⚠️  File not found: {filepath}")
            continue
        
        splitter.stats['files_processed'] += 1
        result = splitter.process_file(filepath)
        
        if result is not None:
            splitter.save_file(result, filepath)
    
    print("\n" + "="*80)
    print("✅ PROCESSING COMPLETE")
    print("="*80)
    print(f"\nFiles processed: {splitter.stats['files_processed']}")
    print(f"Rows split: {splitter.stats['rows_split']}")
    print(f"New rows created: {splitter.stats['new_rows_created']}")
    print(f"\nSplit files saved in: ./split_emails/")
    print("\n💡 TIP: Review the split files to ensure they meet your needs.")
    print("    You can now use these for one-to-one email outreach.")

if __name__ == "__main__":
    main()

