#!/usr/bin/python

import argparse
import requests
import json
import os.path
import logging
from datetime import datetime
import csv
import tomllib
from lib.anything_llm_ai import anything_llm_ai_thread_setup, create_new_anythingllm_workspace_ai, create_new_workspace_thread, delete_workspace, delete_all_workspaces, list_workspaces, chat_with_model_in_thread_ai
from lib.anything_llm_sales import anything_llm_sales_thread_setup, create_new_anythingllm_workspace_sales, create_new_workspace_thread, delete_workspace, delete_all_workspaces, list_workspaces, chat_with_model_in_thread_sales
from lib.anything_llm_devops import anything_llm_devops_thread_setup, create_new_anythingllm_workspace_devops, create_new_workspace_thread, delete_workspace, delete_all_workspaces, list_workspaces, chat_with_model_in_thread_devops
from lib.pretalx import write_out_data, get_submissions
from lib.sessionize import get_submissions_sessionize

start_time = datetime.now()
logging.basicConfig(filename="log/main_logging.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

PRETALX_TOKEN=config["PRETALX_TOKEN"]
PRETALX_URL=config["PRETALX_URL"]
PRETALX_EVENT=config["PRETALX_EVENT"]
SAVEFILE=config["SAVEFILE"]

SESSIONIZE_API=config["SESSIONIZE_API"]

ANYTHINGLLM_APIKEY=config["ANYTHINGLLM_APIKEY"]
ANYTHINGLLM_URL=config["ANYTHINGLLM_URL"]


def read_csv_file(CSV_FILE):
    with open(CSV_FILE, "r") as f:
        data = csv.DictReader(f)
        data_list = []
        for row in data:
            data_list.append(row)
    return data_list


def main():
    raw_data = None

    parser = argparse.ArgumentParser(description="Have your local LLM catigorize somethings for you")

    parser.add_argument("-c", "--csv", type=str, help="csv to run against")
    parser.add_argument("-d", "--delete", action='store_true', help=f"delete workspaces in AnythingLLM from {ANYTHINGLLM_URL} api")
    parser.add_argument("-p", "--pretalx", action='store_true', help=f"pull from the pretalx {PRETALX_URL} api")
    parser.add_argument("-s", "--sessionize", action='store_true', help=f"pull from the sessionize {SESSIONIZE_API} api")
    parser.add_argument("-w", "--workspace", action='store_true', help=f"set up a workspace in AnythingLLM at {ANYTHINGLLM_URL}")
    parser.add_argument("--devops", action='store_true', help=f"run the devopsdays checks against the abstracts")

    args = parser.parse_args()

    if args.delete:
        delete_all_workspaces() # this is here because you're lazy
        print("*****")
        print("Deleted all the workspaces in AnythingLLM...")
        print("*****")
        exit()

    if args.csv:
        CSV_FILE=args.csv
        raw_data = read_csv_file(CSV_FILE)
        backend = "the csv file you submited"

    if args.pretalx:
        data_pretalx = get_submissions(PRETALX_TOKEN, PRETALX_URL, PRETALX_EVENT)
        write_out_data(SAVEFILE, data_pretalx)

        with open(SAVEFILE, 'r') as f:
            data = json.load(f)

        raw_data = data['results']
        backend = f"your configured pretalx instance here {PRETALX_URL}"

    if args.sessionize:
        data_sessionize = get_submissions_sessionize(SESSIONIZE_API)
        write_out_data(SAVEFILE, data_sessionize)

        with open(SAVEFILE, 'r') as f:
            data = json.load(f)

        raw_data = data['sessions']
        backend = f"your configured sessionize instance here {SESSIONIZE_API}"

    if args.workspace:
        print("*****")
        print(f"Setting up a 'one-off' workspace for you in AnythingLLM at {ANYTHINGLLM_URL}...it can take a second...")
        print("*****")
        create_new_anythingllm_workspace_ai(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, "one-off-ai")
        anything_llm_ai_thread_setup("one-off-ai")
        create_new_anythingllm_workspace_sales(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, "one-off-sales")
        anything_llm_sales_thread_setup("one-off-sales")
        create_new_anythingllm_workspace_devops(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, "one-off-devops")
        anything_llm_sales_thread_setup("one-off-devops")
        exit()


    if raw_data == None:
        print("******")
        print("You need to either input a csv, pull fom pretalx or sessionize to get the abstracts")
        print("Run the script with `-h` to give you the options")
        print("******")
        exit(1)

    key = input(f"""
*****
We are going to check the next {len(raw_data)} abstracts from {backend} against the LLM now,
press enter continue or 'q' to just quit...
*****
""")
    if key == 'q':
        exit()
    else:
        print("Running...")
        with open('overview.csv','w', newline='') as f:
            writer = csv.writer(f)

            if args.devops:
                fields = ["ai_unique_code","title","ai_score","sales_score","accept_score","sales_justification","accept_justification","ai_justification"]
            else:
                fields = ["ai_unique_code","title","ai_score","sales_score","sales_justification","ai_justification"]

            writer.writerow(fields)

        for i in raw_data:
            if args.sessionize:
                unique_code = i['id']
                ai_unique_code = f"{i['id']}-ai"
                sales_unique_code = f"{i['id']}-sales"
                devops_unique_code = f"{i['id']}-devops"
            else:
                unique_code = i['code']
                ai_unique_code = f"{i['code']}-ai"
                sales_unique_code = f"{i['code']}-sales"
                devops_unique_code = f"{i['code']}-devops"

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

            try:
                abstract = i['abstract']
            except KeyError as e:
                abstract = None

            if abstract == None or len(abstract) <= len(description):
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

                if ai_score >= 90:
                    print("")
                    print("****AI Suspect****")
                    print(f"TITLE: {i['title']}")
                    print(f"UNIQUE CODE: {ai_unique_code}")
                    print(f"SCORE: {ai_score}")
                    print(f"JUSTIFICATION: {ai_justification}")
                    print("*******")
                    print("")
            except:
                ai_score = "n/a"
                ai_justification = abstract_response.json()['textResponse'].partition(".")[2].strip()

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

            try:
                abstract = i['abstract']
            except KeyError as e:
                abstract = None

            if abstract == None or len(abstract) <= len(description):
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

                if sales_score > 75:
                    print("")
                    print("****Sales Pitch Suspect****")
                    print(f"TITLE: {i['title']}")
                    print(f"UNIQUE CODE: {sales_unique_code}")
                    print(f"SCORE: {sales_score}")
                    print(f"JUSTIFICATION: {sales_justification}")
                    print("*******")
                    print("")
            except:
                sales_score = "n/a"
                sales_justification = abstract_response.json()['textResponse'].partition(".")[2].strip()

            if args.devops:
                delete_workspace(devops_unique_code)
                create_new_anythingllm_workspace_devops(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, devops_unique_code)

                anything_llm_devops_thread_setup(devops_unique_code)

                logging.info("")
                logging.info("*******")
                logging.info(f"TITLE: {i['title']}")

                try:
                    description = i['description']
                except KeyError as e:
                    description = "None"

                try:
                    abstract = i['abstract']
                except KeyError as e:
                    abstract = None

                if abstract == None or len(abstract) <= len(description):
                    abstract = i['description']
                else:
                    abstract = i['abstract']
                devops_abstract_response = chat_with_model_in_thread_devops(devops_unique_code, devops_unique_code, abstract)
                devops_justification = devops_abstract_response.json()['textResponse']
                logging.info(justification)
                logging.info("*******")
                logging.info("")
                try:
                    accept_score = int(devops_abstract_response.json()['textResponse'].partition("%")[0].strip())
                    accept_justification = devops_abstract_response.json()['textResponse'].partition("%")[2].strip()

                    if accept_score > 90:
                        print("")
                        print("!!!!!High possibility of Acceptance!!!!!")
                        print(f"TITLE: {i['title']}")
                        print(f"UNIQUE CODE: {devops_unique_code}")
                        print(f"SCORE: {accept_score}")
                        print(f"JUSTIFICATION: {accept_justification}")
                        print("*******")
                        print("")
                except:
                    accept_score = "n/a"
                    accept_justification = abstract_response.json()['textResponse'].partition(".")[2].strip()

            with open('overview.csv','a') as f:
                writer = csv.writer(f)
                if args.devops:
                    writer.writerow([f"{unique_code}",f"{i['title']}",f"{ai_score}",f"{sales_score}",f"{accept_score}",f"{sales_justification}",f"{accept_justification}",f"{ai_justification}"])
                else:
                    writer.writerow([f"{unique_code}",f"{i['title']}",f"{ai_score}",f"{sales_score}",f"{sales_justification}",f"{ai_justification}"])


        print(f"This took {datetime.now() - start_time} to run")
        logging.info(f"This took {datetime.now() - start_time} to run")
if __name__ == "__main__":
    main()

