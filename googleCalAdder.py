from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sportradarAPIGrabber as F1Sched

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    # Taken from Google Calendar API Documentation.
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        calendar_id = add_calendar(service)

        # Gets the dictionary created by the sportradarAPIGrabber script
        schedule_org = F1Sched.create_schedule()

        events = []

        ''' 
        Processes the schedule and creates an 'event' in the format
        of Google Calendar API's events. Each event is added to the
        events array 
        '''
        for round in schedule_org:

            timezone = round["time_zone"]

            p1 = {}
            p1["summary"] = round["round_name"] + r" - Practice 1"
            p1["start"] = {"dateTime": round["practice_1"]["start"],
                           "timeZone": timezone}
            p1["end"] = {"dateTime": round["practice_1"]["end"],
                         "timeZone": timezone}
            events.append(p1)

            p2 = {}
            p2["summary"] = round["round_name"] + r" - Practice 2"
            p2["start"] = {"dateTime": round["practice_2"]["start"],
                           "timeZone": timezone}
            p2["end"] = {"dateTime": round["practice_2"]["end"],
                         "timeZone": timezone}
            events.append(p2)

            p3 = {}
            p3["summary"] = round["round_name"] + r" - Practice 3"
            p3["start"] = {"dateTime": round["practice_3"]["start"],
                           "timeZone": timezone}
            p3["end"] = {"dateTime": round["practice_3"]["end"],
                         "timeZone": timezone}
            events.append(p3)

            quali = {}
            quali["summary"] = round["round_name"] + r" - Qualifying"
            quali["start"] = {"dateTime": round["qualification"]["start"],
                              "timeZone": timezone}
            quali["end"] = {"dateTime": round["qualification"]["end"],
                            "timeZone": timezone}
            events.append(quali)

            race = {}
            race["summary"] = round["round_name"] + r" - Race"
            race["start"] = {"dateTime": round["race"]["start"],
                             "timeZone": timezone}
            race["end"] = {"dateTime": round["race"]["end"],
                           "timeZone": timezone}
            events.append(race)

        # Creates each event in the events list
        for event in events:
            print(event["summary"])
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


# Creates an empty calendar in Google Calendar
def add_calendar(service):
    F1_cal = {
        'summary': 'F1 2022',
        'timeZone': 'America/New_York'
    }

    created_calendar = service.calendars().insert(body=F1_cal).execute()

    return created_calendar['id']


if __name__ == '__main__':
    main()
