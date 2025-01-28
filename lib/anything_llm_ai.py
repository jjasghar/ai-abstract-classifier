#!/usr/bin/python
import requests
import json
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

ANYTHINGLLM_APIKEY=config["ANYTHINGLLM_APIKEY"]
ANYTHINGLLM_URL=config["ANYTHINGLLM_URL"]

#WORKSPACE_NAME=config["WORKSPACE_NAME"]
#THREAD_SLUG=config["THREAD_SLUG"]

def anything_llm_ai_thread_setup(unique_code):
    chat_with_model(unique_code)
    create_new_workspace_thread(unique_code,unique_code)
    show_model_100_ai_written(unique_code, unique_code)
    show_model_0_ai_written(unique_code, unique_code)

def create_new_anythingllm_workspace_ai(ANYTHINGLLM_APIKEY, ANYTHINGLLM_URL, name):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "name": name,
       "similarityThreshold": 0.7,
       "openAiTemp": 0.7,
       "openAiHistory": 20,
       "openAiPrompt": "You are an expert reviewer and editor of call for papers, call for presentations, or abstracts for public technical computer and engineering conferences. You know if an submission was written by an AI, and can identify if the submisson has been created by AI. Your job is to rate every submission on a scale of 0 to 100 here 100 is 100% AI written. Please provide the number as a percentage.",
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

def show_model_100_ai_written(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/100_chatgpt.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract written 100% by an AI, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is 100% written by AI. Confirm that you understand that this is not written by a human and is 100% written by AI. Give a justification on why it is 100% written by an AI.\n\n\n ------ \n {data['abstract']}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def show_model_0_ai_written(WORKSPACE_NAME, THREAD_SLUG):
    with open('chat_primes/0_human_written.json', 'r') as f:
        data = json.load(f)
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"The following is an abstract written 0% by an AI, it has the title of: {data['title']} and the following is the abstract. This is a good example of something that is 0% written by AI, and completely written by a human. Confirm that you understand that this is written 100% by a human and is 0% written by AI. Give a justification on why it is 100% written by a human. \n\n\n ------ \n {data['abstract']}.",
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

def chat_with_model_in_thread_ai(WORKSPACE_NAME, THREAD_SLUG, abstract):
    headers = {
            'Authorization': f"Bearer {ANYTHINGLLM_APIKEY}"
    }
    data = {
       "message": f"Read the following abstract and decide a score with a justification on if it was written by an AI. Give the number as a percentage, and provide the justification afterwards. Output your response with the number then a precent sign then a dash with your justification.\n\n\n ------ \n {abstract}.",
       "userId": 1,
       "mode": "chat",
    }
    abstract_response = requests.post(f'{ANYTHINGLLM_URL}/workspace/{WORKSPACE_NAME.lower()}/thread/{THREAD_SLUG.lower()}/chat', headers=headers, data=data)
    return abstract_response

def delete_all_workspaces():
    workspaces = list_workspaces()
    for i in workspaces.json()['workspaces']:
        delete_workspace(i['slug'])
