#!/usr/bin/python

import requests
import json
import os.path
import logging
from datetime import datetime
import csv
import tomllib
from lib.anything_llm_ai import anything_llm_ai_thread_setup, create_new_anythingllm_workspace, create_new_workspace_thread, delete_workspace, delete_all_workspaces, list_workspaces, chat_with_model_in_thread
from lib.pretalx import write_out_data, get_submissions

start_time = datetime.now()
logging.basicConfig(filename="log/logging_logger.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

PRETALX_TOKEN=config["PRETALX_TOKEN"]
PRETALX_URL=config["PRETALX_URL"]
PRETALX_EVENT=config["PRETALX_EVENT"]
SAVEFILE=config["SAVEFILE"]

ANYTHINGLLM_APIKEY=config["ANYTHINGLLM_APIKEY"]
ANYTHINGLLM_URL=config["ANYTHINGLLM_URL"]

#WORKSPACE_NAME=config["WORKSPACE_NAME"]
#THREAD_SLUG=config["THREAD_SLUG"]

def main():

    # need to make this optional when csv importing becomes an option
    data_pretalx = get_submissions(PRETALX_TOKEN, PRETALX_URL, PRETALX_EVENT)
    # check if the json exists, TODO eventually make this csv or json
    if os.path.exists(SAVEFILE):
        with open(SAVEFILE, 'r') as f:
            data = json.load(f)

        if len(data_pretalx['results']) > len(data['results']):
            write_out_data(SAVEFILE, data_pretalx)
            with open(SAVEFILE, 'r') as f:
                data = json.load(f)

        key = input(f"""
*****
We are going to check the next {len(data['results'])} abstracts against the LLM now,
press enter continue or 'd' to quit and delete ALL workspaces or 'q' to just quit...
*****
""")
        if key == 'q':
            exit()
        elif key == 'd':
            delete_all_workspaces() # this is here because you're lazy
            print("*****")
            print("Deleted all the workspaces in AnythingLLM for you. You need to restart the program...")
            print("*****")
            exit()
        else:

            with open('overview.csv','w', newline='') as f:
                writer = csv.writer(f)

                fields = ["unique_code","title","ai_score","ai_justification"]
                writer.writerow(fields)

            for i in data['results']:
                delete_workspace(i['code'])
                create_new_anythingllm_workspace(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, i['code'])

                anything_llm_ai_thread_setup(i['code'])

                logging.info("")
                logging.info("*******")
                logging.info(f"TITLE: {i['title']}")
                if i['abstract'] == None or len(i['abstract']) <= len(i['description']):
                    abstract = i['description']
                else:
                    abstract = i['abstract']
                abstract_response = chat_with_model_in_thread(i['code'], i['code'], abstract)
                justification = abstract_response.json()['textResponse']
                logging.info(justification)
                logging.info("*******")
                logging.info("")

                try:
                    ai_score = int(abstract_response.json()['textResponse'].partition("%")[0].strip())
                    ai_justification = abstract_response.json()['textResponse'].partition("%")[2].strip()
                except:
                    ai_score = int(abstract_response.json()['textResponse'].partition(".")[0].strip())
                    ai_justification = abstract_response.json()['textResponse'].partition(".")[2].strip()

                if ai_score > 75:
                    print("")
                    print("****AI Suspect****")
                    print(f"TITLE: {i['title']}")
                    print(f"UNIQUE CODE: {i['code']}")
                    print(f"SCORE: {ai_score}")
                    print(f"JUSTIFICATION: {ai_justification}")
                    print("*******")
                    print("")

                with open('overview.csv','a') as f:
                    writer = csv.writer(f)
                    writer.writerow([f"{i['code']}",f"{i['title']}",f"{ai_score}",f"{ai_justification}"])



            print(f"This took {datetime.now() - start_time} to run")
            logging.info(f"This took {datetime.now() - start_time} to run")
    else:
    # write out the file0
        write_out_data(SAVEFILE, data_pretalx)
        print("*****")
        print("Looks like you don't have a local json, making one from your pretalx backend")
        print("You'll need to restart the program...")
        print("*****")

if __name__ == "__main__":
    main()

