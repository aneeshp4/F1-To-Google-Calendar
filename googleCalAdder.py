from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sportradarAPIGrabber as F1Sched
import datetime
from tzlocal import get_localzone


SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """ Creates a Google Calendar and populates it with the 2023 F1 schedule"""

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

        # Create the empty calendar
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

            for event in round:
                if event != "round_name" and event != "time_zone":

                    # Create the event in google calendar format
                    event_dict = {}
                    event_dict["summary"] = round["round_name"] + " - " + event
                    event_dict["start"] = {"dateTime": round[event]["start"],
                                           "timeZone": timezone}
                    event_dict["end"] = {"dateTime": round[event]["end"],
                                         "timeZone": timezone}
                    
                    # Add the event to the events list
                    events.append(event_dict)


        # Creates each event in the events list to populate the previously empty calendar
        for event in events:
            print(event["summary"])
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
        print('All events created successfully!')

    except HttpError as error:
        print('An error occurred: %s' % error)


def add_calendar(service):
    """Creates an empty calendar in Google Calendar and returns the calendar's ID"""

    cur_year = datetime.date.today().year
    local_timezone = get_localzone()
    F1_cal = {
        'summary': 'F1 ' + str(cur_year),
        'timeZone': local_timezone
    }

    created_calendar = service.calendars().insert(body=F1_cal).execute()

    return created_calendar['id']


if __name__ == '__main__':
    main()
