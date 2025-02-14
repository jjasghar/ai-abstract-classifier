#!/usr/bin/python
import requests
import json
import tomllib
from lib.utils import create_new_workspace_thread, chat_with_model

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

ANYTHINGLLM_APIKEY=config["ANYTHINGLLM_APIKEY"]
ANYTHINGLLM_URL=config["ANYTHINGLLM_URL"]

def anything_llm_devops_thread_setup(unique_code):
    chat_with_model(unique_code)
    create_new_workspace_thread(unique_code,unique_code)
    show_model_engineering_leadership_devops(unique_code,unique_code)
    show_model_mlops_devops(unique_code,unique_code)
    show_model_pitch_bad_devops(unique_code,unique_code)

def create_new_anythingllm_workspace_devops(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, name):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "name": name,
       "similarityThreshold": 0.7,
       "openAiTemp": 0.7,
       "openAiHistory": 20,
       "openAiPrompt": "You are an expert editor and conference organizer for technical conferences. Your job is to read abstracts and descriptions for possible conference talks at a highly technical conference about DevOps. Read the following abstract and description and give a 0-100% idea of why you would or wouldn’t accept this talk for your event.  Understand that 100% is I would absolutely accept this to the conference, while 0% is there are reasons why I wouldn't.",
       "queryRefusalResponse": "Custom refusal message",
       "chatMode": "chat",
       "topN": 4
    }
    requests.post(f'{ANYTHINGLLM_URL}/workspace/new', headers=headers, data=data)

def show_model_engineering_leadership_devops(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/jsons/100_engineering_leadership.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract is an example of 100% acceptance at your conference, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is 100% acceptance and what we want at our event. Confirm that you understand that this a amazing abstract and give a justification on why it is something you would 100% accept.\n\n\n ------ \n {data['abstract']}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def show_model_mlops_devops(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/jsons/100_mlops_devops.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract is an example of 100% acceptance at your conference, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is 100% acceptance and what we want at our event. Confirm that you understand that this a amazing abstract and give a justification on why it is something you would 100% accept.\n\n\n ------ \n {data['abstract']}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def show_model_pitch_bad_devops(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/jsons/0_bad_devops.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract is an example of 0% acceptance, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is only a 0% and not what we want at our confernce.Confirm that you understand that this a bad submission, and give a justification on why it is only a 0% score.\n\n\n ------ \n {data['abstract']}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def chat_with_model_in_thread_devops(WORKSPACE_NAME, THREAD_SLUG, abstract):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"Read the following abstract and decide a score with a justification on if it a talk that should be accepted to your DevOps Conference. We want anything that is technical or in the spirit of collaboration and the principles of DevOps.. Give the number as a percentage, and provide the justification afterwards. Output your response with the number then a precent sign then a dash with your justification.\n\n\n ------ \n {abstract}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response
