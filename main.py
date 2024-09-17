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

restaurant_data = extract_json_data(restaurant_url)
country_data = pd.read_excel("./data/Country-Code.xlsx")

# To match country code & get country
country_codes = country_data['Country Code'].tolist()
country_dict = country_data.set_index('Country Code')['Country'].to_dict()

# Get restaurant details and events
restaurant_details = []

for i in range(5): # for testing -> range(len(restaurant_data))

    restaurants_list = restaurant_data[i]['restaurants']

    for restaurant in restaurants_list:
        details = restaurant['restaurant']
        
        # Task 1: Only include restaurants with matching country code
        country_id =  details['location']['country_id']
        if country_id in country_codes: 
            event = details.get('zomato_events', None)
            restaurant_details.append({
                'Restaurant Id': details['id'],
                'Restaurant Name': details['name'],
                'Country': country_dict[country_id], 
                'City': details['location']['city'],
                'User Rating Votes': int(details['user_rating']['votes']),
                'User Aggregate Rating': float(details['user_rating']['aggregate_rating']),
                'Cuisines': details['cuisines'],
                'Event Data Extraction': event,
                'Number of Events': len(event)
            })

# Save outputs
restaurant_details_df = pd.DataFrame(restaurant_details)
restaurant_details_df.to_csv('./output/restaurant_details.csv', index=False)

