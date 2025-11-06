"""
Email Bounce Verification Tool
Integrates with professional email verification services to check deliverability
"""

import pandas as pd
import requests
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import re

class EmailBounceChecker:
    """
    Verify emails using multiple verification services
    Supports: ZeroBounce, NeverBounce, Hunter.io, EmailListVerify, Kickbox
    """
    
    def __init__(self):
        self.results = []
        self.stats = {
            'total_checked': 0,
            'valid': 0,
            'risky': 0,
            'invalid': 0,
            'unknown': 0,
            'catch_all': 0,
            'disposable': 0,
            'role_based': 0
        }
        
        # Load API keys from config file
        self.api_keys = self.load_api_keys()
        
    def load_api_keys(self) -> Dict[str, str]:
        """Load API keys from config file"""
        config_file = 'email_verification_config.json'
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Create template config file
            template = {
                "zerobounce_api_key": "YOUR_ZEROBOUNCE_API_KEY_HERE",
                "neverbounce_api_key": "YOUR_NEVERBOUNCE_API_KEY_HERE",
                "hunter_api_key": "YOUR_HUNTER_API_KEY_HERE",
                "emaillistverify_api_key": "YOUR_EMAILLISTVERIFY_API_KEY_HERE",
                "kickbox_api_key": "YOUR_KICKBOX_API_KEY_HERE",
                "service_to_use": "zerobounce"
            }
            
            with open(config_file, 'w') as f:
                json.dump(template, f, indent=2)
            
            print(f"⚙️  Created config file: {config_file}")
            print("📝 Please add your API key(s) to the config file and run again.")
            return template
    
    def verify_with_zerobounce(self, email: str) -> Dict:
        """Verify email using ZeroBounce API"""
        api_key = self.api_keys.get('zerobounce_api_key', '')
        
        if not api_key or api_key == 'YOUR_ZEROBOUNCE_API_KEY_HERE':
            return {'status': 'error', 'sub_status': 'no_api_key'}
        
        url = f"https://api.zerobounce.net/v2/validate"
        params = {
            'api_key': api_key,
            'email': email,
            'ip_address': ''
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'email': email,
                'status': data.get('status', 'unknown'),
                'sub_status': data.get('sub_status', ''),
                'free_email': data.get('free_email', False),
                'did_you_mean': data.get('did_you_mean', ''),
                'mx_found': data.get('mx_found', ''),
                'smtp_provider': data.get('smtp_provider', ''),
                'service': 'zerobounce'
            }
        except Exception as e:
            return {'email': email, 'status': 'error', 'error': str(e), 'service': 'zerobounce'}
    
    def verify_with_neverbounce(self, email: str) -> Dict:
        """Verify email using NeverBounce API"""
        api_key = self.api_keys.get('neverbounce_api_key', '')
        
        if not api_key or api_key == 'YOUR_NEVERBOUNCE_API_KEY_HERE':
            return {'status': 'error', 'sub_status': 'no_api_key'}
        
        url = "https://api.neverbounce.com/v4/single/check"
        params = {
            'key': api_key,
            'email': email
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = data.get('result', 'unknown')
            
            # Map NeverBounce results to standard statuses
            status_map = {
                'valid': 'valid',
                'invalid': 'invalid',
                'disposable': 'disposable',
                'catchall': 'catch_all',
                'unknown': 'unknown'
            }
            
            return {
                'email': email,
                'status': status_map.get(result, 'unknown'),
                'flags': data.get('flags', []),
                'suggested_correction': data.get('suggested_correction', ''),
                'service': 'neverbounce'
            }
        except Exception as e:
            return {'email': email, 'status': 'error', 'error': str(e), 'service': 'neverbounce'}
    
    def verify_with_hunter(self, email: str) -> Dict:
        """Verify email using Hunter.io API"""
        api_key = self.api_keys.get('hunter_api_key', '')
        
        if not api_key or api_key == 'YOUR_HUNTER_API_KEY_HERE':
            return {'status': 'error', 'sub_status': 'no_api_key'}
        
        url = "https://api.hunter.io/v2/email-verifier"
        params = {
            'email': email,
            'api_key': api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                result = data['data']
                status = result.get('status', 'unknown')
                
                # Map Hunter statuses
                status_map = {
                    'valid': 'valid',
                    'invalid': 'invalid',
                    'accept_all': 'catch_all',
                    'webmail': 'valid',
                    'disposable': 'disposable',
                    'unknown': 'unknown'
                }
                
                return {
                    'email': email,
                    'status': status_map.get(status, 'unknown'),
                    'score': result.get('score', 0),
                    'regexp': result.get('regexp', False),
                    'gibberish': result.get('gibberish', False),
                    'disposable': result.get('disposable', False),
                    'webmail': result.get('webmail', False),
                    'mx_records': result.get('mx_records', False),
                    'smtp_server': result.get('smtp_server', False),
                    'smtp_check': result.get('smtp_check', False),
                    'service': 'hunter'
                }
            else:
                return {'email': email, 'status': 'error', 'error': 'No data returned', 'service': 'hunter'}
        except Exception as e:
            return {'email': email, 'status': 'error', 'error': str(e), 'service': 'hunter'}
    
    def verify_with_kickbox(self, email: str) -> Dict:
        """Verify email using Kickbox API"""
        api_key = self.api_keys.get('kickbox_api_key', '')
        
        if not api_key or api_key == 'YOUR_KICKBOX_API_KEY_HERE':
            return {'status': 'error', 'sub_status': 'no_api_key'}
        
        url = f"https://api.kickbox.com/v2/verify"
        params = {
            'email': email,
            'apikey': api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = data.get('result', 'unknown')
            
            # Map Kickbox results
            status_map = {
                'deliverable': 'valid',
                'undeliverable': 'invalid',
                'risky': 'risky',
                'unknown': 'unknown'
            }
            
            return {
                'email': email,
                'status': status_map.get(result, 'unknown'),
                'reason': data.get('reason', ''),
                'role': data.get('role', False),
                'free': data.get('free', False),
                'disposable': data.get('disposable', False),
                'accept_all': data.get('accept_all', False),
                'sendex': data.get('sendex', 0),
                'service': 'kickbox'
            }
        except Exception as e:
            return {'email': email, 'status': 'error', 'error': str(e), 'service': 'kickbox'}
    
    def verify_email(self, email: str, service: str = None) -> Dict:
        """Verify a single email using specified service"""
        if service is None:
            service = self.api_keys.get('service_to_use', 'zerobounce')
        
        service_map = {
            'zerobounce': self.verify_with_zerobounce,
            'neverbounce': self.verify_with_neverbounce,
            'hunter': self.verify_with_hunter,
            'kickbox': self.verify_with_kickbox
        }
        
        verify_func = service_map.get(service.lower())
        if verify_func:
            return verify_func(email)
        else:
            return {'email': email, 'status': 'error', 'error': 'Unknown service'}
    
    def process_file(self, filepath: str, max_emails: int = None):
        """Process a CSV/Excel file and verify all emails"""
        print(f"\n{'='*80}")
        print(f"Processing: {filepath}")
        print(f"{'='*80}")
        
        try:
            # Read file
            ext = os.path.splitext(filepath)[1].lower()
            
            if ext == '.csv':
                df = pd.read_csv(filepath, encoding='utf-8')
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath)
            else:
                print(f"❌ Unsupported file type: {ext}")
                return None
            
            # Find email column
            email_col = None
            for col in df.columns:
                if 'email' in str(col).lower():
                    email_col = col
                    break
            
            if not email_col:
                print("❌ No email column found")
                return None
            
            print(f"📧 Email column: {email_col}")
            print(f"📊 Total emails to verify: {len(df)}")
            
            if max_emails:
                print(f"⚠️  Limiting to first {max_emails} emails")
                df = df.head(max_emails)
            
            # Get unique emails
            unique_emails = df[email_col].dropna().unique()
            print(f"📧 Unique emails: {len(unique_emails)}")
            
            # Verify each email
            results = []
            service = self.api_keys.get('service_to_use', 'zerobounce')
            
            print(f"\n🔍 Starting verification using {service}...")
            print("⏳ This may take a while...\n")
            
            for idx, email in enumerate(unique_emails, 1):
                print(f"  [{idx}/{len(unique_emails)}] Checking: {email}...", end=' ')
                
                result = self.verify_email(email, service)
                results.append(result)
                
                status = result.get('status', 'unknown')
                status_emoji = {
                    'valid': '✅',
                    'invalid': '❌',
                    'risky': '⚠️',
                    'catch_all': '📬',
                    'disposable': '🗑️',
                    'unknown': '❓',
                    'error': '⚠️'
                }
                
                print(f"{status_emoji.get(status, '❓')} {status}")
                
                # Update stats
                self.stats['total_checked'] += 1
                if status in self.stats:
                    self.stats[status] += 1
                
                # Rate limiting - be nice to the API
                time.sleep(0.1)  # 100ms between requests
            
            # Create results dataframe
            results_df = pd.DataFrame(results)
            
            # Merge with original data
            df_verified = df.merge(
                results_df,
                left_on=email_col,
                right_on='email',
                how='left',
                suffixes=('', '_verification')
            )
            
            return df_verified
            
        except Exception as e:
            print(f"❌ Error processing file: {str(e)}")
            return None
    
    def save_verified_file(self, df: pd.DataFrame, original_path: str):
        """Save verified results"""
        try:
            output_dir = "verified_emails"
            os.makedirs(output_dir, exist_ok=True)
            
            base_name = os.path.basename(original_path)
            name_without_ext = os.path.splitext(base_name)[0]
            ext = os.path.splitext(base_name)[1].lower()
            
            # Clean up filename
            name_without_ext = re.sub(r'_CLEANED_\d{8}_\d{6}', '', name_without_ext)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{name_without_ext}_VERIFIED_{timestamp}{ext}"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save
            if ext == '.csv':
                df.to_csv(output_path, index=False, encoding='utf-8')
            elif ext in ['.xlsx', '.xls']:
                df.to_excel(output_path, index=False, engine='openpyxl')
            
            print(f"\n💾 Saved verified file: {output_path}")
            
            # Also save low-risk only version
            if 'status' in df.columns:
                df_safe = df[df['status'].isin(['valid'])]
                
                safe_filename = f"{name_without_ext}_LOW_RISK_{timestamp}{ext}"
                safe_path = os.path.join(output_dir, safe_filename)
                
                if ext == '.csv':
                    df_safe.to_csv(safe_path, index=False, encoding='utf-8')
                elif ext in ['.xlsx', '.xls']:
                    df_safe.to_excel(safe_path, index=False, engine='openpyxl')
                
                print(f"💾 Saved low-risk file: {safe_path}")
                print(f"   📊 Low-risk contacts: {len(df_safe)} (from {len(df)} total)")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")
            return None
    
    def generate_report(self):
        """Generate verification report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"bounce_verification_report_{timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("EMAIL BOUNCE VERIFICATION REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("VERIFICATION STATISTICS\n")
            f.write("-"*80 + "\n")
            f.write(f"Total emails checked: {self.stats['total_checked']}\n")
            f.write(f"Valid (Safe to send): {self.stats['valid']} ({self.stats['valid']/max(self.stats['total_checked'],1)*100:.1f}%)\n")
            f.write(f"Invalid (Will bounce): {self.stats['invalid']} ({self.stats['invalid']/max(self.stats['total_checked'],1)*100:.1f}%)\n")
            f.write(f"Risky (May bounce): {self.stats['risky']} ({self.stats['risky']/max(self.stats['total_checked'],1)*100:.1f}%)\n")
            f.write(f"Catch-all (Unknown): {self.stats['catch_all']} ({self.stats['catch_all']/max(self.stats['total_checked'],1)*100:.1f}%)\n")
            f.write(f"Disposable: {self.stats['disposable']} ({self.stats['disposable']/max(self.stats['total_checked'],1)*100:.1f}%)\n")
            f.write(f"Unknown: {self.stats['unknown']} ({self.stats['unknown']/max(self.stats['total_checked'],1)*100:.1f}%)\n\n")
            
            f.write("RECOMMENDATIONS\n")
            f.write("-"*80 + "\n")
            f.write("✅ Valid: Safe to send - use these contacts\n")
            f.write("❌ Invalid: Will bounce - remove from list\n")
            f.write("⚠️  Risky: May bounce - use with caution or remove\n")
            f.write("📬 Catch-all: Server accepts all emails - monitor closely\n")
            f.write("🗑️  Disposable: Temporary email - remove from list\n")
            f.write("❓ Unknown: Verification failed - manual review needed\n")
        
        print(f"\n📊 Report saved: {report_path}")
        return report_path


def main():
    """Main execution"""
    print("="*80)
    print("EMAIL BOUNCE VERIFICATION TOOL")
    print("="*80)
    print("\n⚠️  IMPORTANT: This tool requires an API key from a verification service.")
    print("Recommended services (sorted by value):")
    print("  1. ZeroBounce - https://www.zerobounce.net/ (Best accuracy, $16/1k emails)")
    print("  2. NeverBounce - https://neverbounce.com/ ($8/1k emails)")
    print("  3. Hunter.io - https://hunter.io/ (50 free/month, then $49/month)")
    print("  4. Kickbox - https://kickbox.com/ (100 free, then $10/1k emails)")
    print("\n💡 TIP: Most services offer free trials or credits to start!\n")
    
    checker = EmailBounceChecker()
    
    # Check if API key is configured
    service = checker.api_keys.get('service_to_use', 'zerobounce')
    api_key = checker.api_keys.get(f'{service}_api_key', '')
    
    if not api_key or 'YOUR_' in api_key:
        print("❌ No API key configured!")
        print(f"📝 Please edit 'email_verification_config.json' and add your API key.")
        print(f"   Then set 'service_to_use' to your preferred service.")
        return
    
    print(f"✅ Using service: {service}")
    print(f"📁 Looking for cleaned files...\n")
    
    # Get cleaned files
    cleaned_dir = "cleaned_leads"
    
    if not os.path.exists(cleaned_dir):
        print(f"❌ Directory not found: {cleaned_dir}")
        print("Please run verify_and_clean_emails.py first!")
        return
    
    # Priority files to verify
    priority_files = [
        "Hotels_ICP_High_Value_Prospects_v2_CLEANED_*.csv",
        "Hotels_ICP_Boutique_Luxury_v2_CLEANED_*.csv",
        "Hubspot_Import_FINAL_20251016_CLEANED_*.csv",
        "Priority_Contact_List_CLEANED_*.csv",
    ]
    
    print("📋 Processing priority files:")
    print("  1. High Value Prospects")
    print("  2. Boutique Luxury")
    print("  3. Hubspot Import")
    print("  4. Priority Contact List")
    print("\n⚠️  Note: This will use API credits. Proceed? (y/n): ", end='')
    
    # For automation, you can comment out this input and set proceed = 'y'
    proceed = input().lower()
    
    if proceed != 'y':
        print("❌ Verification cancelled.")
        return
    
    # Find and process files
    import glob
    
    for pattern in priority_files:
        files = glob.glob(os.path.join(cleaned_dir, pattern.replace('*', '*')))
        
        for filepath in files:
            result_df = checker.process_file(filepath, max_emails=None)  # Set max_emails=50 for testing
            
            if result_df is not None:
                checker.save_verified_file(result_df, filepath)
    
    # Generate report
    checker.generate_report()
    
    print("\n" + "="*80)
    print("✅ BOUNCE VERIFICATION COMPLETE")
    print("="*80)
    print(f"\nTotal emails checked: {checker.stats['total_checked']}")
    print(f"✅ Valid (low bounce risk): {checker.stats['valid']}")
    print(f"❌ Invalid (high bounce risk): {checker.stats['invalid']}")
    print(f"⚠️  Risky: {checker.stats['risky']}")
    print(f"\nVerified files saved in: ./verified_emails/")
    print(f"Low-risk files (valid only) also saved separately!")


if __name__ == "__main__":
    main()

