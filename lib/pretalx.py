import requests
import tomllib
import json

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

PRETALX_TOKEN=config["PRETALX_TOKEN"]
PRETALX_URL=config["PRETALX_URL"]
PRETALX_EVENT=config["PRETALX_EVENT"]
SAVEFILE=config["SAVEFILE"]


def write_out_data(SAVEFILE, data):
    with open(f'{SAVEFILE}','w') as f:
        json.dump(data, f)

def get_submissions(PRETALX_TOKEN, PRETALX_URL, PRETALX_EVENT):
    payload = {
            'Authorization': f"{PRETALX_TOKEN}",
    }
    try:
        r = requests.get(f'{PRETALX_URL}/api/me', headers=payload)

        if r.status_code == 200:
            # this is a hack, you pull _all_ of the submissions, if you have
            # over 10000 you're one hellva conference.
            submissions_r = requests.get(f'{PRETALX_URL}/api/events/{PRETALX_EVENT}/submissions?limit=10000', headers=payload)
            data = submissions_r.json()
            return data
    except:
        print("*****")
        print("***** You couldn't get to the sumbissions for _reasons_.")
        print("*****")
        exit(1)

