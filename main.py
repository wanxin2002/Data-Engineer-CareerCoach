import requests
import pandas as pd
from datetime import datetime


# Helper functions
def extract_json_data(url):
    response = requests.get(url)
    if response.status_code == 200: 
        data = response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
    return data


def event_in_apr_2019(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Range needed
    apr_start = datetime(2019, 4, 1)
    apr_end = datetime(2019, 4, 30)
    
    return start_date <= apr_end and end_date >= apr_start


#%% Main
# Data extraction
restaurant_url = 'https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json'
restaurant_data = extract_json_data(restaurant_url)
country_data = pd.read_excel("./data/Country-Code.xlsx")

# To match country code & get country
country_codes = country_data['Country Code'].tolist()
country_dict = country_data.set_index('Country Code')['Country'].to_dict()

# Get restaurant details and events
restaurant_details = []
restaurant_events = []

for i in range(len(restaurant_data)):

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
                'Number of Events': len(event) if event is not None else 0
            })
        

        # Task 2: Only include events in Apr 2019
        if 'zomato_events' in details:
            event_list = details['zomato_events']

            for event in event_list:
                event_data = event['event']
                start_date = event_data['start_date']
                end_date = event_data['end_date']

                if event_in_apr_2019(start_date, end_date): 
                    restaurant_events.append({
                        'Event Id': event_data['event_id'],
                        'Restaurant Id': details['id'],
                        'Restaurant Name': details['name'],
                        'Photo URL': details['photos_url'], 
                        'Event Title': event_data['title'],
                        'Event Start Date': start_date,
                        'Event End Date': end_date
                    })


# Save outputs
restaurant_details_df = pd.DataFrame(restaurant_details)
restaurant_details_df.to_csv('./output/restaurant_details.csv', index=False)

restaurant_events_df = pd.DataFrame(restaurant_events)
restaurant_events_df.to_csv('./output/restaurant_events.csv', index=False)

