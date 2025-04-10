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

# main.py

import os
import sys
from datacleanerPackage.datacleaner import *

def main():
    """
    Main entry point for the fuel data cleaning application.
    """
    print("Starting fuel data processing...")
    
    # Determine absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "Data")
    
    # Verify Data directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created Data directory: {data_dir}")
    else:
        print(f"Data directory exists: {data_dir}")
    
    # Verify input file exists
    input_file = os.path.join(data_dir, "fuel_data.csv")
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        print("Please place your CSV file in the Data folder.")
        return
    else:
        print(f"Input file found: {input_file}")
    
    # Set up output paths
    cleaned_file = os.path.join(data_dir, "cleanedData.csv")
    anomalies_file = os.path.join(data_dir, "dataAnomalies.csv")
    
    # Initialize API client and processor
    api_key = 'e978c950-162b-11f0-97f0-e96660f7696c'
    api_client = ZipCodeAPI(api_key)
    processor = DataCleaner(api_client)
    
    # Process data
    processor.process_csv(input_file)
    processor.write_output(cleaned_file, anomalies_file)
    
    print("\nProcessing complete!")
    print(f"Cleaned data saved to: {cleaned_file}")
    print(f"Anomalies saved to: {anomalies_file}")

if __name__ == '__main__':
    main()
