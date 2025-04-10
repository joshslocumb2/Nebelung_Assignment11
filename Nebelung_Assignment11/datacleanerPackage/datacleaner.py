# File Name: Nebelung_Assignment11
# Student Name: Josh Slocumb, Caitlin Hutchins
# email: slocumbjt@mail.uc.edu, hutchicu@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date: 4/10/2025
# Course #/Section: IS 4010-001
# Semester/Year:Spring 2025
# Brief Description of the assignment: 

# Brief Description of what this module does. {Do not copy/paste from a previous assignment. Put some thought into this. required}
# Citations: {"Stack Overflow" is not sufficient. Provide repeatable links, book page #, etc.}

# Anything else that's relevant:

# datacleaner.py



# datacleaner.py
import csv
import os
import re

class DataCleaner:
    """
    Main data processing class handling CSV cleaning operations.
    """
    
    def __init__(self, api_client):
        """Initialize with API client and data structures"""
        self.api_client = api_client
        self.cleaned_data = []
        self.anomalies = []
        self.seen_records = set()
        self.missing_zip_count = 0
        
    def _extract_city_state(self, address):
        """
        Extract city and state from address string.
        
        Args:
            address (str): Full address
            
        Returns:
            tuple: (city, state) or ('', '') if not found
        """
        # Simple pattern matching - assuming format "... City, State zip"
        try:
            match = re.search(r'([^,]+),\s*([A-Z]{2})', address)
            if match:
                return match.group(1).strip(), match.group(2).strip()
        except:
            pass
        return '', ''
        
    def _has_zip_code(self, address):
        """Check if address already has zip code"""
        return bool(re.search(r'\b\d{5}\b', address))
        
    def _process_zip_code(self, row):
        """Handle missing zip codes with API lookup"""
        if 'Full Addre' in row and not self._has_zip_code(row['Full Addre']) and self.missing_zip_count < 5:
            city, state = self._extract_city_state(row['Full Addre'])
            if city and state:
                print(f"Looking up ZIP for {city}, {state}")
                zip_code = self.api_client.get_zip_code(city, state)
                if zip_code:
                    row['Full Addre'] = f"{row['Full Addre']} {zip_code}"
                    self.missing_zip_count += 1
                    print(f"Updated address with ZIP: {row['Full Addre']}")
        return row
        
    def _process_pricing(self, row):
        """Standardize gross price formatting to exactly 2 decimal places"""
        try:
            if 'Gross Pric' in row:
                # Remove currency symbols and commas, then convert to float
                price_str = row['Gross Pric'].replace('$', '').replace(',', '')
                price = float(price_str)
                # Format to exactly 2 decimal places
                row['Gross Pric'] = f"{price:.2f}"
        except Exception as e:
            print(f"Error processing price: {e}")
        return row
        
    def _create_record_hash(self, row):
        """Create a unique hash for the record to identify duplicates"""
        # Create a tuple of values and hash it
        values = tuple(str(v) for v in row.values())
        return hash(values)
        
    def process_row(self, row):
        """
        Main processing pipeline for individual records.
        
        Args:
            row (dict): CSV row data
            
        Returns:
            dict or None: Processed row or None if it's a duplicate or Pepsi
        """
        # Check if this is a Pepsi purchase
        if 'Fuel Type' in row and row['Fuel Type'].strip().lower() == 'pepsi':
            print(f"Found Pepsi purchase: {row['Transactio']}")
            self.anomalies.append(row)
            return None
            
        # Process the row
        row = self._process_zip_code(row)
        row = self._process_pricing(row)
        
        # Check for duplicates
        row_hash = self._create_record_hash(row)
        if row_hash in self.seen_records:
            print(f"Found duplicate: {row['Transactio']}")
            return None
            
        # Add to seen records and return
        self.seen_records.add(row_hash)
        return row
        
    def process_csv(self, input_path):
        """Process the entire CSV file"""
        print(f"Processing CSV file: {input_path}")
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                print(f"CSV headers: {headers}")
                
                for row in reader:
                    processed = self.process_row(row)
                    if processed:
                        self.cleaned_data.append(processed)
                        
            print(f"Processed {len(self.cleaned_data)} valid records and {len(self.anomalies)} anomalies")
                        
        except FileNotFoundError:
            print(f"Error: CSV file not found at {input_path}")
        except Exception as e:
            print(f"Error processing CSV: {str(e)}")
            
    def write_output(self, clean_path, anomaly_path):
        """Write processed data to output files"""
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(clean_path), exist_ok=True)
        
        # Write cleaned data
        if self.cleaned_data:
            try:
                with open(clean_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.cleaned_data[0].keys())
                    writer.writeheader()
                    writer.writerows(self.cleaned_data)
                print(f"Wrote {len(self.cleaned_data)} records to {clean_path}")
            except Exception as e:
                print(f"Error writing cleaned data: {str(e)}")
        else:
            print("No clean records to write")
        
        # Write anomalies
        if self.anomalies:
            try:
                with open(anomaly_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.anomalies[0].keys())
                    writer.writeheader()
                    writer.writerows(self.anomalies)
                print(f"Wrote {len(self.anomalies)} anomalies to {anomaly_path}")
            except Exception as e:
                print(f"Error writing anomalies: {str(e)}")
        else:
            print("No anomalies to write")
