import requests
import json
import tomllib

with open("config.toml", "rb") as f:
        config = tomllib.load(f)

        ANYTHINGLLM_APIKEY=config["ANYTHINGLLM_APIKEY"]
        ANYTHINGLLM_URL=config["ANYTHINGLLM_URL"]

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

def delete_all_workspaces():
    workspaces = list_workspaces()
    for i in workspaces.json()['workspaces']:
        delete_workspace(i['slug'])
