import http.client
import os
import json
from dotenv import load_dotenv
import pprint
# Load .env file and get API key
load_dotenv()
key = os.getenv("SPORT_RADAR_API_KEY")

# Establish connection to Sport Radar API
conn = http.client.HTTPSConnection("api.sportradar.com")

def get_request(url):
    """Makes a GET request to the Sport Radar API and returns the response as a dictionary/json"""
    conn.request(
        "GET", url)
    res = conn.getresponse()
    data = res.read()
    dict = json.loads(data.decode('utf-8'))

    return dict

def get_current_year_id():
    """Gets the current year's ID from the API to be used to get the current season's schedule"""

    url = "/formula1/trial/v2/en/seasons.json?api_key=" + str(key)
    dict = get_request(url)
    return dict['stages'][0]['id']

def create_schedule():
    """Gets the current season's schedule from the API and returns it as a dictionary"""

    # Get season schedule URL
    season_2023_id = get_current_year_id()
    season_schedule_url = "/formula1/trial/v2/en/sport_events/" + season_2023_id + "/schedule.json?api_key=" + str(key)
    unorganized = get_request(season_schedule_url)

    schedules_organized = []

    for round in unorganized["stages"]:

        if round["status"] != "Cancelled":
            
            events = {}
            events["round_name"] = round["description"]

            # Monaco was missing its timezone in the API, so I manually added it
            if round["venue"]["country"] == "Monaco":
                events["time_zone"] = "Europe/Monaco"
            else:
                events["time_zone"] = round["venue"]["timezone"]

            for event in round['stages']:
                events[event['description']] = {}
                events[event['description']]["start"] = event["scheduled"]
                events[event['description']]["end"] = event["scheduled_end"]
            

            schedules_organized.append(events)

    return schedules_organized