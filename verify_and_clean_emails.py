import pandas as pd
import re
import os
from datetime import datetime
import json

class EmailVerifier:
    """Comprehensive email verification and cleanup utility"""
    
    def __init__(self):
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        self.stats = {
            'total_files': 0,
            'total_rows': 0,
            'total_emails_found': 0,
            'valid_emails': 0,
            'invalid_emails': 0,
            'missing_emails': 0,
            'duplicates_removed': 0,
            'cleaned_files': []
        }
        self.all_emails = {}  # Track emails across all files
        self.issues = []
        
    def is_valid_email(self, email):
        """Validate email format"""
        if pd.isna(email) or email == '' or email is None:
            return False, "missing"
        
        email_str = str(email).strip().lower()
        
        # Check for common invalid patterns
        if email_str in ['nan', 'none', '-', 'n/a', 'na']:
            return False, "missing"
        
        # Check format
        if not self.email_pattern.match(email_str):
            return False, "invalid_format"
        
        # Check for common typos
        if '.con' in email_str or ',com' in email_str:
            return False, "typo"
        
        # Check for suspicious patterns
        if email_str.count('@') != 1:
            return False, "multiple_at"
        
        if email_str.startswith('@') or email_str.endswith('@'):
            return False, "invalid_format"
        
        return True, "valid"
    
    def clean_email(self, email):
        """Attempt to clean/fix common email issues"""
        if pd.isna(email) or email == '':
            return None
        
        email_str = str(email).strip().lower()
        
        # Fix common typos
        email_str = email_str.replace(',com', '.com')
        email_str = email_str.replace('.con', '.com')
        email_str = email_str.replace(' ', '')
        
        # Remove multiple spaces
        email_str = re.sub(r'\s+', '', email_str)
        
        # Validate cleaned email
        is_valid, _ = self.is_valid_email(email_str)
        return email_str if is_valid else None
    
    def process_csv_file(self, filepath):
        """Process a CSV file"""
        print(f"\n{'='*80}")
        print(f"Processing: {filepath}")
        print(f"{'='*80}")
        
        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    df = pd.read_csv(filepath, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print(f"❌ Could not read file with any encoding: {filepath}")
                return None
            
            return self.process_dataframe(df, filepath)
            
        except Exception as e:
            print(f"❌ Error processing {filepath}: {str(e)}")
            return None
    
    def process_excel_file(self, filepath):
        """Process an Excel file"""
        print(f"\n{'='*80}")
        print(f"Processing: {filepath}")
        print(f"{'='*80}")
        
        try:
            # Read all sheets
            xls = pd.ExcelFile(filepath)
            all_dfs = []
            
            for sheet_name in xls.sheet_names:
                print(f"\n  📋 Sheet: {sheet_name}")
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                df['_source_sheet'] = sheet_name
                all_dfs.append(df)
            
            if all_dfs:
                combined_df = pd.concat(all_dfs, ignore_index=True)
                return self.process_dataframe(combined_df, filepath)
            
        except Exception as e:
            print(f"❌ Error processing {filepath}: {str(e)}")
            return None
    
    def process_dataframe(self, df, filepath):
        """Process a dataframe and clean emails"""
        file_stats = {
            'file': filepath,
            'original_rows': len(df),
            'email_columns': [],
            'valid_emails': 0,
            'invalid_emails': 0,
            'missing_emails': 0,
            'duplicates': 0,
            'cleaned_rows': 0
        }
        
        # Find email columns
        email_columns = []
        for col in df.columns:
            col_lower = str(col).lower()
            if 'email' in col_lower or 'e-mail' in col_lower or 'mail' in col_lower:
                email_columns.append(col)
        
        if not email_columns:
            print(f"  ℹ️  No email columns found")
            return None
        
        print(f"  📧 Email columns found: {', '.join(email_columns)}")
        file_stats['email_columns'] = email_columns
        
        # Process each email column
        for email_col in email_columns:
            print(f"\n  🔍 Analyzing column: {email_col}")
            
            original_emails = df[email_col].copy()
            valid_count = 0
            invalid_count = 0
            missing_count = 0
            issues_in_col = []
            
            # Check each email
            for idx, email in enumerate(original_emails):
                is_valid, reason = self.is_valid_email(email)
                
                if reason == "missing":
                    missing_count += 1
                elif reason == "valid":
                    valid_count += 1
                    cleaned = self.clean_email(email)
                    df.at[idx, email_col] = cleaned
                    
                    # Track across all files
                    if cleaned:
                        if cleaned in self.all_emails:
                            self.all_emails[cleaned].append(filepath)
                        else:
                            self.all_emails[cleaned] = [filepath]
                else:
                    invalid_count += 1
                    issues_in_col.append({
                        'row': idx + 2,  # +2 for header and 0-index
                        'email': email,
                        'reason': reason
                    })
                    # Try to clean
                    cleaned = self.clean_email(email)
                    if cleaned:
                        df.at[idx, email_col] = cleaned
                        print(f"    ✓ Fixed: '{email}' → '{cleaned}'")
            
            print(f"    ✅ Valid: {valid_count}")
            print(f"    ❌ Invalid: {invalid_count}")
            print(f"    ⚠️  Missing: {missing_count}")
            
            file_stats['valid_emails'] += valid_count
            file_stats['invalid_emails'] += invalid_count
            file_stats['missing_emails'] += missing_count
            
            # Show some invalid examples
            if issues_in_col:
                print(f"\n    📋 Sample issues (showing first 10):")
                for issue in issues_in_col[:10]:
                    print(f"       Row {issue['row']}: '{issue['email']}' - {issue['reason']}")
                self.issues.extend(issues_in_col)
        
        # Remove duplicates within this file
        original_len = len(df)
        
        # Remove rows where all email columns are empty
        email_mask = df[email_columns].notna().any(axis=1)
        df_with_emails = df[email_mask].copy()
        
        # Remove duplicate emails (keep first occurrence)
        if email_columns:
            df_cleaned = df_with_emails.drop_duplicates(subset=email_columns, keep='first')
        else:
            df_cleaned = df_with_emails
        
        duplicates_removed = original_len - len(df_cleaned)
        file_stats['duplicates'] = duplicates_removed
        file_stats['cleaned_rows'] = len(df_cleaned)
        
        print(f"\n  🧹 Cleanup summary:")
        print(f"     Original rows: {original_len}")
        print(f"     Rows without email: {original_len - len(df_with_emails)}")
        print(f"     Duplicate rows removed: {duplicates_removed}")
        print(f"     Final cleaned rows: {len(df_cleaned)}")
        
        self.stats['total_rows'] += original_len
        self.stats['total_emails_found'] += (file_stats['valid_emails'] + file_stats['invalid_emails'])
        self.stats['valid_emails'] += file_stats['valid_emails']
        self.stats['invalid_emails'] += file_stats['invalid_emails']
        self.stats['missing_emails'] += file_stats['missing_emails']
        self.stats['duplicates_removed'] += duplicates_removed
        
        return df_cleaned, file_stats
    
    def save_cleaned_file(self, df, original_path, file_stats):
        """Save cleaned dataframe to a new file"""
        try:
            # Create output directory
            output_dir = "cleaned_leads"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output filename
            base_name = os.path.basename(original_path)
            name_without_ext = os.path.splitext(base_name)[0]
            ext = os.path.splitext(base_name)[1].lower()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{name_without_ext}_CLEANED_{timestamp}{ext}"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save based on file type
            if ext == '.csv':
                df.to_csv(output_path, index=False, encoding='utf-8')
            elif ext in ['.xlsx', '.xls']:
                df.to_excel(output_path, index=False, engine='openpyxl')
            
            print(f"\n  💾 Saved cleaned file: {output_path}")
            file_stats['output_file'] = output_path
            self.stats['cleaned_files'].append(file_stats)
            
            return output_path
            
        except Exception as e:
            print(f"  ❌ Error saving file: {str(e)}")
            return None
    
    def generate_report(self):
        """Generate comprehensive verification report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"email_verification_report_{timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("EMAIL VERIFICATION & CLEANUP REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall Statistics
            f.write("OVERALL STATISTICS\n")
            f.write("-"*80 + "\n")
            f.write(f"Total files processed: {self.stats['total_files']}\n")
            f.write(f"Total rows processed: {self.stats['total_rows']}\n")
            f.write(f"Total emails found: {self.stats['total_emails_found']}\n")
            f.write(f"Valid emails: {self.stats['valid_emails']}\n")
            f.write(f"Invalid emails: {self.stats['invalid_emails']}\n")
            f.write(f"Missing emails: {self.stats['missing_emails']}\n")
            f.write(f"Duplicates removed: {self.stats['duplicates_removed']}\n\n")
            
            # File-by-file breakdown
            f.write("\nFILE-BY-FILE BREAKDOWN\n")
            f.write("="*80 + "\n")
            for file_stat in self.stats['cleaned_files']:
                f.write(f"\nFile: {file_stat['file']}\n")
                f.write(f"  Original rows: {file_stat['original_rows']}\n")
                f.write(f"  Cleaned rows: {file_stat['cleaned_rows']}\n")
                f.write(f"  Email columns: {', '.join(file_stat['email_columns'])}\n")
                f.write(f"  Valid emails: {file_stat['valid_emails']}\n")
                f.write(f"  Invalid emails: {file_stat['invalid_emails']}\n")
                f.write(f"  Missing emails: {file_stat['missing_emails']}\n")
                f.write(f"  Duplicates removed: {file_stat['duplicates']}\n")
                f.write(f"  Output file: {file_stat.get('output_file', 'N/A')}\n")
            
            # Cross-file duplicates
            f.write("\n\nCROSS-FILE DUPLICATE ANALYSIS\n")
            f.write("="*80 + "\n")
            duplicates = {email: files for email, files in self.all_emails.items() if len(files) > 1}
            
            if duplicates:
                f.write(f"Found {len(duplicates)} emails appearing in multiple files:\n\n")
                for email, files in sorted(duplicates.items()):
                    f.write(f"  {email}\n")
                    for file in files:
                        f.write(f"    - {file}\n")
            else:
                f.write("No cross-file duplicates found.\n")
            
            # Common issues
            if self.issues:
                f.write("\n\nCOMMON EMAIL ISSUES\n")
                f.write("="*80 + "\n")
                issue_types = {}
                for issue in self.issues:
                    reason = issue['reason']
                    if reason not in issue_types:
                        issue_types[reason] = []
                    issue_types[reason].append(issue)
                
                for reason, issues in issue_types.items():
                    f.write(f"\n{reason.upper()} ({len(issues)} occurrences):\n")
                    for issue in issues[:20]:  # Show first 20 of each type
                        f.write(f"  {issue['email']}\n")
        
        print(f"\n📊 Detailed report saved: {report_path}")
        return report_path

def main():
    """Main execution function"""
    print("="*80)
    print("EMAIL VERIFICATION & CLEANUP TOOL")
    print("="*80)
    
    verifier = EmailVerifier()
    
    # Define files to process
    leads_files = [
        # Hotel ICP files
        'Hotels_ICP_High_Value_Prospects_v2.csv',
        'Hotels_ICP_Associate_Partners_v2.csv',
        'Hotels_ICP_Boutique_Luxury_v2.csv',
        'Hotels_ICP_Budget_Large_v2.csv',
        'Hotels_ICP_Budget_Small_v2.csv',
        'Hotels_ICP_Mid_Tier_Prospects_v2.csv',
        'Hotels_ICP_Other_v2.csv',
        'Hotels_ICP_Small_Properties_v2.csv',
        'Hotels_ICP_Unknown_v2.csv',
        'Hotels_ICP_Segmented_Master_v2.csv',
        
        # MAH Members
        'MAH_Members_Directory_Complete_2025.csv',
        'MAH_Members_Directory_2025.csv',
        
        # Hubspot imports
        'Hubspot_Import_FINAL_20251016.csv',
        'Hubspot_Import_Complete_All_Quotes_20251015_180901_CLEANED.csv',
        
        # Priority lists
        'Priority_Contact_List.csv',
        
        # Other leads
        'originistudios_leads_final.csv',
        'hotels_directory_with_id.csv',
        
        # Excel event responses
        'APHM 30 May - 1 June 2023 (Responses).xlsx',
        'APHM 4 June - 6 June 2024 (Responses).xlsx',
        'APHM 9 June - 11 June 2025 (Responses).xlsx',
        'ASTA E-Invoice Customer Data (Responses).xlsx',
        'FHA HoReCa Questionnaire (Responses).xlsx',
        'FHMB2024 (Responses).xlsx',
        'FHT2022.xlsx',
        'FHT2024 (Responses).xlsx',
        'FHV 2022 Questionnaire (Responses).xlsx',
        'Food & Hotel Indonesia 2023 (Responses).xlsx',
        'MyBha Johor 10 May 2023 (Responses).xlsx',
        'Questionnaire_ Food & Hotel Malaysia 2023 (Responses).xlsx',
        
        # FHM Leads files
        'Leads - FHM 2025_FINAL_20251016.xlsx',
        'Leads - FHM 2025_FINAL_CLEAN_20251016_095205.xlsx',
        'Leads - FHM 2025.xlsx',
        'Leads - MAH - High_Value_Prospects.xlsx',
    ]
    
    # Process each file
    for filename in leads_files:
        if not os.path.exists(filename):
            print(f"\n⚠️  File not found: {filename}")
            continue
        
        verifier.stats['total_files'] += 1
        
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.csv':
            result = verifier.process_csv_file(filename)
        elif ext in ['.xlsx', '.xls']:
            result = verifier.process_excel_file(filename)
        else:
            print(f"⚠️  Unsupported file type: {filename}")
            continue
        
        if result:
            df_cleaned, file_stats = result
            verifier.save_cleaned_file(df_cleaned, filename, file_stats)
    
    # Generate final report
    print("\n" + "="*80)
    print("GENERATING FINAL REPORT")
    print("="*80)
    verifier.generate_report()
    
    print("\n" + "="*80)
    print("✅ EMAIL VERIFICATION & CLEANUP COMPLETE")
    print("="*80)
    print(f"\nProcessed {verifier.stats['total_files']} files")
    print(f"Total rows: {verifier.stats['total_rows']}")
    print(f"Valid emails: {verifier.stats['valid_emails']}")
    print(f"Invalid emails: {verifier.stats['invalid_emails']}")
    print(f"Duplicates removed: {verifier.stats['duplicates_removed']}")
    print(f"\nCleaned files saved in: ./cleaned_leads/")

if __name__ == "__main__":
    main()

