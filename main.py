import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os
import logging
import urllib.parse

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set API details
api_key = os.getenv('API_TOKEN')
company_id = os.getenv('COMPANY_ID')
limit = 200
start_date = '2024-09-01T03:00:00.000Z'
end_date = '2024-09-10T02:59:00.000Z'
queues = 'ADagendaCo,ADagendaJu,ADfinan,ADposvendaCo,ADposvendaJu,COcontabilAM,COcontabilES,COcontabilMT,COcontabilRR,COjuridico,SUcontabil,SUcontabilSp,SUescrita,SUescritaSim,SUfolha,SUfolhaDctfF,SUfolhaInteg,SUlegalone,SUtecnica,SUtecnicaOnb,SUtecnicaOnv,SUtecnicaOut,SUtecnicaSer,SUtecOnvMess,SUtecOnvPort'

def fetch_queue_performance(api_token, company_id, start_date, end_date, queues, tme_target, tma_target):
    headers = {
        'api_token': api_token
    }
    
    params = {
        'companyId': company_id,
        'createdAtGt': start_date,
        'createdAtLt': end_date,
        'queues': queues,
        'slaTmeTarget': tme_target,
        'slaTmaTarget': tma_target
    }
    
    try:
        api_url = 'https://callreport.opens.com.br/call/queue-performance'
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        json_data = response.json()

        print('\n')
        print( urllib.parse.unquote( response.url ) )
        print('documentCount: ' + str(json_data['documentCount']))
        print('\n')

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching queue performance data: {e}")

def fetch_page(api_token, limit, start_date, end_date, queues, search_after0, search_after1, company_id):
    headers = {
        'api_token': api_token
    }
    
    params = {
        'limit': limit,
        'createdAtGt': start_date,
        'createdAtLt': end_date,
        'queues': queues,
        'companyId': company_id
    }
    
    if search_after1:
        params['searchAfter[0]'] = search_after0 
        params['searchAfter[1]'] = search_after1

    try:
        api_url = 'https://callreport.opens.com.br/call/scroll'
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        if not response.json().get('sort'):
            print('\n')
            print( urllib.parse.unquote( response.url ) )
            print('\n')
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

def extract_calls(data):
    return [
        {
            'id': call.get('id'),
            'callId': call.get('callId'),
            'totalDuration': call.get('totalDuration'),
            'linkedId': call.get('linkedId'),
            'answeredAt': call.get('answeredAt'),
            'type': call.get('type'),
            'createdAt': call.get('createdAt'),
            'protocol': call.get('protocol'),
            'totalTalkTime': call.get('totalTalkTime'),
            'totalWaitTime': call.get('totalWaitTime'),
            'elasticId': call.get('elasticId'),
            'hungupAt': call.get('hungupAt'),
            'updatedAt': call.get('updatedAt')
        }
        for call in data
    ]

# Fetch queue performance data
fetch_queue_performance(api_key, company_id, start_date, end_date, queues, 1200, 1200)

# Main loop to fetch data
fetched_data = []
search_after0 = ''
search_after1 = ''
has_more_data = True

while has_more_data:
    json_data = fetch_page(api_key, limit, start_date, end_date, queues, search_after0, search_after1, company_id)
    
    if json_data and 'data' in json_data and json_data['data']:
        fetched_data.extend(extract_calls(json_data['data']))

        # Update searchAfter for next page if available
        search_after0 = json_data.get('sort')[0] if json_data.get('sort') else None
        search_after1 = json_data.get('sort')[1] if json_data.get('sort') else None
        has_more_data = search_after1 is not None

        logging.info(f"Fetched lines so far: {len(fetched_data)}")
        time.sleep(1)  # Respect server rate limits
    else:
        has_more_data = False

# Convert data to a CSV using pandas
if fetched_data:
    output_filename = f'call-scroll-{start_date.split("T")[0]}-{end_date.split("T")[0]}.csv'
    df = pd.DataFrame(fetched_data)
    df.to_csv(output_filename, index=False)
    logging.info(f'Data has been successfully written to {output_filename}')
else:
    logging.warning('No data was fetched.')