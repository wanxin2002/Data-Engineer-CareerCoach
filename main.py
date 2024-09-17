import requests
import pandas as pd


# Data extraction
restaurant_url = 'https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json'

def extract_json_data(url):
    response = requests.get(url)
    if response.status_code == 200: 
        data = response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
    return data

restaurant_data = extract_json_data(restaurant_url)[0] # Get the 1st element (dictionary) of the list
country_data = pd.read_excel("./data/Country-Code.xlsx")




