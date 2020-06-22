from fastapi import FastAPI, WebSocket, Body
from fastapi.responses import HTMLResponse
from schemes import *
import requests
import json
import time

ports = json.load(open('../urls.json'))
users = {}

app = FastAPI()

ner_url = f"http://localhost:{ports['ner']}/"
algo_url = f"http://localhost{ports['algo']}/"

def fetch_user(name=None, token=None):
    if token is None:
        token = name
    if token not in users:
        users[token] = User(token=token)
    return users[token]

def add_replic_to_history(replic):
    pass

def change_user_state(token, state):
    users[token].state = state

@app.post('/auth')
def auth_user(name: str = Body(..., embed=True)):
    user = fetch_user(name=name)
    return {"token": user.token}

@app.post("/reply") # add more decorators
def reply(token: str = Body(..., embed=True), \
          text: str = Body(..., embed=True)):
    user = fetch_user(token=token)
    speech = Speech(**requests.get(ner_url, json={"text": text}))
    replic = Replic(author=Author(is_user=True, _id=user.token), # user._id
                    timestamp=time.time(), # make timezone agnostic
                    speech=speech)
    add_replic_to_history(replic)
    if user.state.dialog_skill_id == "":
        response = requests.get(algo_url, json={'replic': replic.as_dict()})
        algo = response['']

    return
