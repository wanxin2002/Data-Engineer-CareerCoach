import requests
import pandas as pd
from datetime import datetime


# Helper functions
def extract_json_data(url):
    response = requests.get(url)
    if response.status_code == 200: 
        data = response.json()
    else:
        print(f'Failed to fetch data. Status code: {response.status_code}')
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
country_data = pd.read_excel('./data/Country-Code.xlsx')

# To match country code & get country
country_codes = country_data['Country Code'].tolist()
country_dict = country_data.set_index('Country Code')['Country'].to_dict()

# Get restaurant details and events
restaurant_details = []    # task 1
restaurant_events = []     # task 2
rating_data = []           # task 3

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
        
        # Task 3: Collect aggregate_rating and rating_text
        rating_text = details['user_rating']['rating_text'].lower()
        aggregate_rating = float(details['user_rating']['aggregate_rating'])

        ## Categorize rating text
        if rating_text in ['excellent', 'eccellente', 'excelente', 'terbaik']:
            category = 'Excellent'
        elif rating_text in ['very good', 'bardzo dobrze', 'muito bom', 
                             'muy bueno', 'velmi dobré']:
            category = 'Very good'
        elif rating_text in ['good', 'bueno']:
            category = 'Good'
        elif rating_text in ['average']:
            category = 'Average'
        elif rating_text in ['poor']:
            category = 'Poor'
        else:
            category = None

        rating_data.append({
            'Rating text': rating_text,
            'Aggregate rating': aggregate_rating,
            'Category': category
        })

# Ratings analysis
rating_df = pd.DataFrame(rating_data)
rating_stats = (
    rating_df
    .groupby('Category')['Aggregate rating']
    .agg(['min', 'max', 'mean', 'median'])
    .sort_values(by='min')
)
print('General statistics:')
print(rating_stats)
print('As seen from the statistics, thresholds for each rating text \
      can be determined by the minimum and maximum aggregated rating \
      for each group. See README.md for the final thresholds determined.')


# Save outputs
restaurant_details_df = pd.DataFrame(restaurant_details)
restaurant_details_df.fillna('NA', inplace=True)
restaurant_details_df.to_csv('./output/restaurant_details.csv', index=False)

restaurant_events_df = pd.DataFrame(restaurant_events)
restaurant_events_df.fillna('NA', inplace=True)
restaurant_events_df.to_csv('./output/restaurant_events.csv', index=False)

rating_df.to_csv('./output/ratings.csv', index=False)
