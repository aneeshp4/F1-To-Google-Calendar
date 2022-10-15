import http.client
import json

conn = http.client.HTTPSConnection("api.sportradar.com")

key_dict = json.load(open("sportradarAPIkey.json"))
key = key_dict["key"]

season_2022_id = "sr:stage:937183"
season_schedule_url = "/formula1/trial/v2/en/sport_events/" + \
    season_2022_id + "/schedule.json?api_key=" + str(key)


# Gets API requests and stores them as dictionaries
def get_request(url):

    conn.request(
        "GET", url)
    res = conn.getresponse()
    data = res.read()
    dict = json.loads(data.decode('utf-8'))

    return dict


# Gets schedule from API and parses necessary information into a dictionary
def create_schedule():
    unorganized = get_request(season_schedule_url)

    schedules_organized = []

    for round in unorganized["stages"]:

        if round["status"] != "Cancelled":
            events = {}
            events["round_name"] = round["description"]

            if round["venue"]["country"] == "France":
                events["time_zone"] = "Europe/Paris"
            elif round["venue"]["country"] == "Monaco":
                events["time_zone"] = "Europe/Monaco"
            else:
                events["time_zone"] = round["venue"]["timezone"]

            events["practice_1"] = {}
            events["practice_1"]["start"] = round["stages"][0]["scheduled"]
            events["practice_1"]["end"] = round["stages"][0]["scheduled_end"]

            events["practice_2"] = {}
            events["practice_2"]["start"] = round["stages"][1]["scheduled"]
            events["practice_2"]["end"] = round["stages"][1]["scheduled_end"]

            events["practice_3"] = {}
            events["practice_3"]["start"] = round["stages"][2]["scheduled"]
            events["practice_3"]["end"] = round["stages"][2]["scheduled_end"]

            events["qualification"] = {}
            events["qualification"]["start"] = round["stages"][3]["scheduled"]
            events["qualification"]["end"] = round["stages"][3]["scheduled_end"]

            events["race"] = {}
            events["race"]["start"] = round["stages"][4]["scheduled"]
            events["race"]["end"] = round["stages"][4]["scheduled_end"]

            schedules_organized.append(events)

    return schedules_organized
