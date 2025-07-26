import csv
import os
import re
from datetime import datetime

class SteamCSVCleaner:
    """Clean Steam CSV files by removing unwanted entries like refunds, gifts, market transactions, etc."""
    
    def __init__(self, input_file):
        self.input_file = input_file
        self.encoding = self._detect_encoding()
        self.rows = []
        self.removal_stats = {
            'empty_refunds': 0,
            'refund_pairs': 0,
            'gifts': 0,
            'gift_blocks': 0,
            'wallet_purchases': 0,
            'wallet_credits': 0,
            'market_transactions': 0,
            'currency_conversions': 0
        }
    
    def _detect_encoding(self):
        """Detect the encoding of the CSV file."""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(self.input_file, 'r', encoding=encoding) as f:
                    f.read()
                print(f"✅ Detected encoding: {encoding}")
                return encoding
            except UnicodeDecodeError:
                continue
        
        print(f"⚠️  Using fallback encoding: utf-8")
        return 'utf-8'
    
    def _load_data(self):
        """Load CSV data into memory."""
        with open(self.input_file, 'r', encoding=self.encoding) as f:
            self.rows = list(csv.reader(f))
    
    def _has_date(self, row):
        """Check if a row starts with a date."""
        if not row or not row[0].strip():
            return False
        
        date_patterns = [
            r'\d{1,2}-[A-Za-z]{3}-\d{2,4}',  # 7-Dec-24
            r'\d{1,2}/\d{1,2}/\d{2,4}',      # 7/12/24
            r'\d{4}-\d{1,2}-\d{1,2}',        # 2024-12-07
        ]
        
        return any(re.match(pattern, row[0].strip()) for pattern in date_patterns)
    
    def _extract_amount(self, amount_str):
        """Extract numeric value from amount string."""
        if not amount_str:
            return 0.0
        
        clean_str = re.sub(r'[^\d\.\-\(\)]', '', amount_str)
        
        if '(' in clean_str and ')' in clean_str:
            clean_str = clean_str.replace('(', '').replace(')', '')
            negative = True
        else:
            negative = clean_str.startswith('-')
            clean_str = clean_str.lstrip('-')
        
        try:
            value = float(clean_str)
            return -value if negative else value
        except ValueError:
            return 0.0
    
    def _game_names_match(self, name1, name2):
        """Check if two game names refer to the same game."""
        # Clean and normalize names
        clean1 = re.sub(r'[^\w\s]', '', name1.lower().replace('refund', '').strip())
        clean2 = re.sub(r'[^\w\s]', '', name2.lower().strip())
        
        if len(clean1) > 3 and clean1 in clean2:
            return True
        if len(clean2) > 3 and clean2 in clean1:
            return True
        
        # Check word similarity
        words1 = set(clean1.split())
        words2 = set(clean2.split())
        
        if not words1 or not words2:
            return False
        
        similarity = len(words1.intersection(words2)) / max(len(words1), len(words2))
        return similarity >= 0.7
    
    def _find_refund_pairs(self):
        """Find purchase-refund pairs that should both be removed."""
        data_rows = self.rows[1:]  # Skip header
        refunds = []
        purchases = []
        
        # Separate refunds and purchases
        for i, row in enumerate(data_rows):
            if len(row) < 3:
                continue
                
            items = row[1].strip()
            type_col = row[2].strip()
            
            # Skip empty items and gifts
            if not items or any(x in items.lower() or x in type_col.lower() 
                              for x in ['gift', '(gift)', '- gift']):
                continue
            
            if 'refund' in type_col.lower():
                refunds.append((i, row))
            elif 'purchase' in type_col.lower():
                purchases.append((i, row))
        
        # Find matching pairs
        pairs_to_remove = set()
        
        for refund_idx, refund_row in refunds:
            refund_items = refund_row[1].strip()
            refund_amount = self._extract_amount(refund_row[3] if len(refund_row) > 3 else "")
            
            for purchase_idx, purchase_row in purchases:
                if purchase_idx in pairs_to_remove:
                    continue
                
                purchase_items = purchase_row[1].strip()
                purchase_amount = self._extract_amount(purchase_row[3] if len(purchase_row) > 3 else "")
                
                if (self._game_names_match(refund_items, purchase_items) and 
                    abs(refund_amount - purchase_amount) < 0.01):
                    
                    pairs_to_remove.add(refund_idx)
                    pairs_to_remove.add(purchase_idx)
                    print(f"📝 Found refund pair: {purchase_items[:30]}... ${purchase_amount:.2f}")
                    break
        
        return pairs_to_remove
    
    def _should_remove_row(self, row_idx, row, refund_pairs, skip_gift_block):
        """Determine if a row should be removed and why."""
        if len(row) < 3:
            return False, None, skip_gift_block
        
        items = row[1].strip()
        type_col = row[2].strip()
        total = row[3].strip() if len(row) > 3 else ""
        
        # Handle gift block skipping
        if skip_gift_block:
            if self._has_date(row):
                skip_gift_block = False
            else:
                return True, "Gift Block", skip_gift_block
        
        # Check removal criteria in order of priority
        
        # 1. Refund pairs (both purchase and refund)
        if (row_idx - 1) in refund_pairs:  # Adjust for header
            return True, "Refund Pair", skip_gift_block
        
        # 2. Empty items or standalone refunds
        if not items or 'refund' in items.lower() or 'refund' in type_col.lower():
            return True, "Empty/Refund", skip_gift_block
        
        # 3. Gift purchases (start gift block skipping)
        if ('gift purchase' in type_col.lower() or 
            any(x in items.lower() or x in type_col.lower() 
                for x in ['gift', '(gift)', '- gift'])):
            skip_gift_block = True
            return True, "Gift Purchase", skip_gift_block
        
        # 4. Wallet credit purchases
        if 'purchased' in items.lower() and 'wallet credit' in items.lower():
            return True, "Wallet Purchase", skip_gift_block
        
        # 5. Other unwanted entries
        removal_checks = [
            ('wallet' in type_col.lower() and 'credit' in total.lower(), "Wallet Credit"),
            ('market transaction' in items.lower(), "Market Transaction"),
            ('steam community market' in items.lower(), "Market Transaction"),
            ('conversion' in type_col.lower(), "Currency Conversion")
        ]
        
        for condition, reason in removal_checks:
            if condition:
                return True, reason, skip_gift_block
        
        return False, None, skip_gift_block
    
    def preview_changes(self):
        """Preview what lines would be removed without making changes."""
        print(f"🔍 Preview of changes for: {self.input_file}")
        print("=" * 60)
        
        self._load_data()
        refund_pairs = self._find_refund_pairs()
        
        lines_to_remove = []
        skip_gift_block = False
        
        for i, row in enumerate(self.rows[1:], 1):  # Skip header
            should_remove, reason, skip_gift_block = self._should_remove_row(
                i, row, refund_pairs, skip_gift_block)
            
            if should_remove:
                lines_to_remove.append((i + 1, row[:4], reason))
        
        # Calculate statistics
        stats = {}
        for _, _, reason in lines_to_remove:
            reason_key = reason.lower().replace(' ', '_').replace('/', '_')
            stats[reason_key] = stats.get(reason_key, 0) + 1
        
        print(f"📋 Total lines in file: {len(self.rows) - 1}")
        print(f"🗑️  Lines that would be removed: {len(lines_to_remove)}")
        
        if lines_to_remove:
            print(f"\nRemoval breakdown:")
            for reason, count in stats.items():
                print(f"   📊 {reason.replace('_', ' ').title()}: {count}")
            
            print(f"\nFirst 10 lines to be removed:")
            for line_num, row_data, reason in lines_to_remove[:10]:
                print(f"   Line {line_num} ({reason}): {', '.join(str(cell) for cell in row_data)}")
            
            if len(lines_to_remove) > 10:
                print(f"   ... and {len(lines_to_remove) - 10} more lines")
        
        return len(lines_to_remove)
    
    def clean_file(self, output_file=None):
        """Clean the CSV file and save to output file."""
        if not output_file:
            base_name = os.path.splitext(self.input_file)[0]
            extension = os.path.splitext(self.input_file)[1]
            output_file = f"{base_name}_cleaned{extension}"
        
        self._load_data()
        refund_pairs = self._find_refund_pairs()
        
        lines_kept = 0
        lines_removed = 0
        skip_gift_block = False
        
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            
            for i, row in enumerate(self.rows):
                # Keep header
                if i == 0:
                    writer.writerow(row)
                    lines_kept += 1
                    continue
                
                # Skip empty rows
                if not row or all(not cell.strip() for cell in row):
                    continue
                
                should_remove, reason, skip_gift_block = self._should_remove_row(
                    i, row, refund_pairs, skip_gift_block)
                
                if should_remove:
                    lines_removed += 1
                    print(f"Removed line {i + 1} ({reason}): {', '.join(row[:4])}")
                else:
                    writer.writerow(row)
                    lines_kept += 1
        
        # Summary
        print(f"\n📊 Cleaning Summary:")
        print(f"   Lines kept: {lines_kept}")
        print(f"   Lines removed: {lines_removed}")
        print(f"   Output file: {output_file}")
        
        if lines_removed > 0:
            print(f"\n🗑️  Removed {lines_removed} unwanted lines including:")
            print("   • Empty items, refunds, and refund pairs")
            print("   • Gift purchases and related entries")
            print("   • Wallet credit purchases and credits")
            print("   • Market transactions and currency conversions")
        
        return output_file

def main():
    """Main function to run the CSV cleaner."""
    csv_file = r'D:\SteamHours\ExcelFiles\Book1.csv'
    
    print("🧹 Steam CSV Cleaner v2.0")
    print("=" * 50)
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        print("Please update the csv_file variable with the correct path.")
        return
    
    cleaner = SteamCSVCleaner(csv_file)
    
    # Preview changes
    lines_to_remove = cleaner.preview_changes()
    
    if lines_to_remove > 0:
        response = input(f"\n❓ Do you want to proceed with cleaning? (y/N): ").lower().strip()
        
        if response in ['y', 'yes']:
            print(f"\n🚀 Cleaning file...")
            cleaned_file = cleaner.clean_file()
            
            if cleaned_file:
                print(f"\n✅ File cleaned successfully!")
                print(f"📄 Original: {csv_file}")
                print(f"📄 Cleaned: {cleaned_file}")
        else:
            print(f"\n🚫 Cleaning cancelled.")
    else:
        print(f"\n✅ No changes needed - file is already clean!")
    
    print(f"\n✨ Done!")

if __name__ == "__main__":
    main()
