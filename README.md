These scripts add all the confirmed Formula 1 events for a year into a user's google calendar.

Just run the "googleCalAdder.py" script to get this done. This will require 2 other JSON files though, one for the credentials for the Google Calendar API, and another for the Sportradar API's key. The Sportradar API does not strictly require a JSON, but I chose to include it in an API, so I didn't have to keep it in the python file. As for the Google Calendar API, you will have to go through setting up the API on the Google Cloud API website.

This script will require a google account, which when the script is run will open a browser tab that asks you to log into your google account. 
