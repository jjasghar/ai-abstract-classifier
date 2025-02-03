#!/usr/bin/python
import requests
import json
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

ANYTHINGLLM_APIKEY=config["ANYTHINGLLM_APIKEY"]
ANYTHINGLLM_URL=config["ANYTHINGLLM_URL"]

def anything_llm_sales_thread_setup(unique_code):
    chat_with_model(unique_code)
    create_new_workspace_thread(unique_code,unique_code)
    show_model_thebigai_sales(unique_code,unique_code)
    show_model_devopsisdead_sales(unique_code,unique_code)
    show_model_logging_sales(unique_code,unique_code)
    show_model_pulumi_sales(unique_code,unique_code)

def create_new_anythingllm_workspace_sales(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, name):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "name": name,
       "similarityThreshold": 0.7,
       "openAiTemp": 0.7,
       "openAiHistory": 20,
       "openAiPrompt": "You are an expert reviewer and editor of call for papers, call for presentations, or abstracts for public technical computer and engineering conferences. You know if an submission was written by a sales person or marketing team, and can identify if the submisson has been created by them. Your job is to rate every submission on a scale of 0 to 100 here 100 is 100% sales or product written. Please provide the number as a percentage.",
       "queryRefusalResponse": "Custom refusal message",
       "chatMode": "chat",
       "topN": 4
    }
    requests.post(f'{ANYTHINGLLM_URL}/workspace/new', headers=headers, data=data)

def chat_with_model(WORKSPACE_NAME):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": "What is Magic The Gathering?",
       "mode": "chat",
       "sessionId": "identifier-to-partition-chats-by-external-id",
    }
    requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/chat', headers=headers, data=data)

def show_model_thebigai_sales(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/jsons/100_thebigai_sales.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract is an example of 100% sales pitch, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is 100% sales pitch and not what we want at our event. Confirm that you understand that this a sales pitch and give a justification on why it is as sales pitch.\n\n\n ------ \n {data['abstract']}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def show_model_devopsisdead_sales(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/jsons/100_devopsisdead_sales.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract is an example of 100% sales pitch, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is 100% sales pitch and not what we want at our event. Confirm that you understand that this a sales pitch and give a justification on why it is as sales pitch.\n\n\n ------ \n {data['abstract']}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def show_model_logging_sales(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/jsons/50_logging_sales.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract is an example of 50% sales pitch, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is only a 50% sales pitch can be accepted with good justifications. Confirm that you understand that this a sales pitch and give a justification on why it is only a 50% sales pitch.\n\n\n ------ \n {data['abstract']}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def show_model_pulumi_sales(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/jsons/75_pulumi_sales.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract is an example of 75% sales pitch, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is only a 75% sales pitch and shouldn't be accepted without extremely positive justifications. Confirm that you understand that this a sales pitch and give a justification on why it is only a 75% sales pitch.\n\n\n ------ \n {data['abstract']}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def create_new_workspace_thread(WORKSPACE_NAME, THREAD_SLUG):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "name": WORKSPACE_NAME.lower(),
       "slug": THREAD_SLUG.lower()
    }
    requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/new', headers=headers, data=data)

def delete_workspace(WORKSPACE_NAME):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    requests.delete(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME}', headers=headers)

def list_workspaces():
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    workspaces = requests.get(f'{ANYTHINGLLM_URL}/workspaces', headers=headers)
    return workspaces

def chat_with_model_in_thread_sales(WORKSPACE_NAME, THREAD_SLUG, abstract):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"Read the following abstract and decide a score with a justification on if it was written by a sales person or is attempting to sell a product. We do not want anything that can be considered a sales pitch in our event. Give the number as a percentage, and provide the justification afterwards. Output your response with the number then a precent sign then a dash with your justification.\n\n\n ------ \n {abstract}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def delete_all_workspaces():
    workspaces = list_workspaces()
    for i in workspaces.json()['workspaces']:
        delete_workspace(i['slug'])
