# F1 To Google Calendar

## What is it?

This project adds the upcoming/current season of Formula 1 events to your google calendar!

## How does it work?

It uses Sport Radar's API to get the actual schedule of the current season. Then, it take this schedule, and passes it into the Google Calendar API to add a calendar with all the Formula 1 events of the current year.

## Usage & Installation Instructions

Before you can use this, ensure you have python 3.10 setup, and ready to use. A working internet connection is also necessary! Also, make sure you are logged into the desired google account you want to add this calendar to in your deafult browser.

We need to set up the environment for these scripts to run:

1. Clone this repository
2. Run `pip install -r requirements.txt` in the command line to install the necessary modules and packages.

Now that the environment is setup, we need to make sure you can use the Sport Radar API. You will need to go to https://developer.sportradar.com/docs/read/Home, click on 'Get Trial Keys' and follow the steps to set up an account and get an API key. Once you have an API key:

1. Create a file called `.env`
2. Type `SPORT_RADAR_API_KEY=<insert your API key here>` in the first line of the `.env` file

With the environment set up and you API key stored. You should be able to run googleCalAdder.py by running:

```
python3 googleCalAdder.py
```

When the script is run for the first time, it will pull up your default browser and ask you to log into your google account, along with asking for permissions.

## File Structure

Once you've followed all the above steps, this is what the project directory will look like:

```bash
- sportradarAPIGrabber.py
- googleCalAdder.py
- requirements.txt
- .env
- .gitignore
```

And once you run the script, two more files will be added:

```bash
- token.json
- credentials.json
```
