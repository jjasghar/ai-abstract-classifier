import requests
import tomllib
import json

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


def get_submissions_sessionize(SESSIONIZE_API):
    try:
        r = requests.get(f'{SESSIONIZE_API}')

        if r.status_code == 200:
            submissions_r = requests.get(f'{SESSIONIZE_API}')
            data = submissions_r.json()
            return data
    except:
        print("*****")
        print("***** You couldn't get to the sumbissions for _reasons_.")
        print("*****")
        exit(1)

