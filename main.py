#!/usr/bin/python

import requests
import json
import os.path
import logging
from datetime import datetime
import csv
import tomllib
from lib.anything_llm_ai import anything_llm_ai_thread_setup, create_new_anythingllm_workspace_ai, create_new_workspace_thread, delete_workspace, delete_all_workspaces, list_workspaces, chat_with_model_in_thread_ai
from lib.anything_llm_sales import anything_llm_sales_thread_setup, create_new_anythingllm_workspace_sales, create_new_workspace_thread, delete_workspace, delete_all_workspaces, list_workspaces, chat_with_model_in_thread_sales
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

CSV_FILE=config['CSV_FILE']

def main():

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r") as f:
            data = csv.DictReader(f)
            data_list = []
            for row in data:
                data_list.append(row)
    else:
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

    if os.path.exists(CSV_FILE):
        raw_data = data_list
    else:
        raw_data = data['results']

    key = input(f"""
*****
We are going to check the next {len(raw_data)} abstracts against the LLM now,
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

            fields = ["ai_unique_code","title","ai_score","sales_score","sales_justification","ai_justification"]
            writer.writerow(fields)



        for i in raw_data:
            ai_unique_code = f"{i['code']}-ai"
            sales_unique_code = f"{i['code']}-sales"

            delete_workspace(ai_unique_code)
            create_new_anythingllm_workspace_ai(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, ai_unique_code)

            anything_llm_ai_thread_setup(ai_unique_code)

            logging.info("")
            logging.info("*******")
            logging.info(f"TITLE: {i['title']}")

            try:
                description = i['description']
            except KeyError as e:
                description = "None"

            if i['abstract'] == None or len(i['abstract']) <= len(description):
                abstract = i['description']
            else:
                abstract = i['abstract']
            abstract_response = chat_with_model_in_thread_ai(ai_unique_code, ai_unique_code, abstract)
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

            if ai_score >= 90:
                print("")
                print("****AI Suspect****")
                print(f"TITLE: {i['title']}")
                print(f"UNIQUE CODE: {ai_unique_code}")
                print(f"SCORE: {ai_score}")
                print(f"JUSTIFICATION: {ai_justification}")
                print("*******")
                print("")

            delete_workspace(sales_unique_code)
            create_new_anythingllm_workspace_sales(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, sales_unique_code)

            anything_llm_sales_thread_setup(sales_unique_code)

            logging.info("")
            logging.info("*******")
            logging.info(f"TITLE: {i['title']}")

            try:
                description = i['description']
            except KeyError as e:
                description = "None"

            if i['abstract'] == None or len(i['abstract']) <= len(description):
                abstract = i['description']
            else:
                abstract = i['abstract']
            abstract_response = chat_with_model_in_thread_sales(sales_unique_code, sales_unique_code, abstract)
            justification = abstract_response.json()['textResponse']
            logging.info(justification)
            logging.info("*******")
            logging.info("")

            try:
                sales_score = int(abstract_response.json()['textResponse'].partition("%")[0].strip())
                sales_justification = abstract_response.json()['textResponse'].partition("%")[2].strip()
            except:
                sales_score = int(abstract_response.json()['textResponse'].partition(".")[0].strip())
                sales_justification = abstract_response.json()['textResponse'].partition(".")[2].strip()

            if sales_score > 75:
                print("")
                print("****Sales Pitch Suspect****")
                print(f"TITLE: {i['title']}")
                print(f"UNIQUE CODE: {sales_unique_code}")
                print(f"SCORE: {sales_score}")
                print(f"JUSTIFICATION: {sales_justification}")
                print("*******")
                print("")

            with open('overview.csv','a') as f:
                writer = csv.writer(f)
                writer.writerow([f"{i['code']}",f"{i['title']}",f"{ai_score}",f"{sales_score}",f"{sales_justification}",f"{ai_justification}"])



        print(f"This took {datetime.now() - start_time} to run")
        logging.info(f"This took {datetime.now() - start_time} to run")
if __name__ == "__main__":
    main()

