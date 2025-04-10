

# File Name: apiclient.py
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

# apiclient.py
import json
import requests

class ZipCodeAPI:
    """
    Handles interactions with the Zipcodebase API to retrieve zip codes.
    """
    
    def __init__(self, api_key):
        """Initialize with API key"""
        self.api_key = api_key
        
    def get_zip_code(self, city, state):
        """
        Retrieves zip code for given city/state pair.
        
        Args:
            city (str): City name
            state (str): State abbreviation
            
        Returns:
            str: First valid zip code or empty string
        """
        try:
            # Matching the format from the example code
            url = "https://app.zipcodebase.com/api/v1/search"
            headers = {
                'apikey': self.api_key
            }
            params = {
                'city': city,
                'state_code': state,
                'country': 'US'
            }
            
            response = requests.get(url, headers=headers, params=params)
            json_string = response.content
            parsed_json = json.loads(json_string)
            
            # Debug output
            print(f"API Response for {city}, {state}: {parsed_json}")
            
            # Extract first zip code from results
            if 'results' in parsed_json and parsed_json['results']:
                return parsed_json['results'][0]['postal_code']
            return ''
            
        except Exception as e:
            print(f"ZIP code lookup failed: {str(e)}")
            return ''
