from dotenv import load_dotenv
import requests
import os
from datetime import datetime

from pprint import pprint
load_dotenv()

app_id = os.getenv('APP_ID')
app_key = os.getenv('APP_KEY')
club_number = os.getenv('CLUB_NUMBER')

async def get_event_types():
    event_type_ids = []
    url = f'https://api.abcfinancial.com/rest/{club_number}/calendars/eventtypes'
    response = requests.get(url, headers = {
        'accept': 'application/json',
        'app_id': app_id,
        'app_key': app_key
    })
    data = response.json()
    events = data.get('eventTypes', [])

    for event in events:
        if event.get('category') == 'class':
            event_type_ids.append(event.get('eventTypeId'))

    return event_type_ids

async def get_calendar_events(eventDateRange: str):
    event_type_ids = await get_event_types()
    fields_to_remove = os.getenv('FIELDS_TO_REMOVE', '').split(',')

    url = f'https://api.abcfinancial.com/rest/{club_number}/calendars/events?eventDateRange={eventDateRange}'
    response = requests.get(url, headers = {
        'accept': 'application/json',
        'app_id': app_id,
        'app_key': app_key
    })
    data = response.json()

    if 'events' in data:
        data['events'] = [event for event in data['events'] if event.get('eventTypeId') in event_type_ids]

    if ('events' in data and fields_to_remove):
        for event in data['events']:
            for field in fields_to_remove:
                event.pop(field.strip(), None)

    if 'events' in data:
        for event in data['events']:
            if 'eventTimestamp' in event:
                timestamp = datetime.fromisoformat(event['eventTimestamp'].replace('Z', '+00:00'))
                event['eventDay'] = timestamp.strftime('%A')

    return {'count': len(data['events']), 'events': data['events']}
