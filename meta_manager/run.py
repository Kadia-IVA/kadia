from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from schemes import *
import requests
import json
import time
import os

users = {}

app = FastAPI()

ner_url = os.getenv("PREPROCESSER_URL", "http://localhost:8081/")
skill_manager_url = os.getenv("SKILL_MANAGER_URL", "http://localhost:8082")

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

def fetch_skill(skill_id):
    pass

def fetch_skill_instance(user, skill):
    pass

def update_instance_state(instance, new_state):
    pass

def add_replic_to_dialog(replic, instance):
    pass

@app.post("/reply") # add more decorators
def reply(token: str = Body(..., embed=True), \
          text: str = Body(..., embed=True)):
    user = fetch_user(token=token)
    speech = Speech(**requests.get(ner_url, json={"text": text}))
    replic = Replic(author=Author(is_user=True, _id=user.token), # user._id
                    timestamp=time.time(), # make timezone agnostic
                    speech=speech)
    add_replic_to_history(replic, user)
    if user.state.dialog_skill_id == "" and "/run" not in speech.raw:
            return "Sorry, I do not understand you. Use /run to start dialog"
    skill_id = user.state.dialog_skill_id
    if "/run" in speech.raw:
        _, skill_id = speech.raw.split()
    skill = fetch_skill()
    instance = fetch_skill_instance(user, skill)
    add_replic_to_dialog(replic, instance)
    change_user_state() # is waiting for response..

    resp = requests.post(skill_manager_url, json={'skill': skill.as_dict(),
                                                  'instance': instance.as_dict()}).json()
    new_state = resp['state']
    update_instance_state(instance, new_state)

    speech = resp['speech']
    if resp['code']:
        """
        -1 - error
        0 - normal return
        1 - positive return
        """
        pass

    if resp['type'] == "dialog+end":
        """
        dialog
        dialog+do-not-understand
        dialog+end
        """
        update_user_state()

    speech = requests.get(ner_url + 'postprocess', json={'replic': replic}).json('replic')
    replic = Replic(..., speech=speech)
    add_replic_to_dialog(replic, instance)
    add_replic_to_history(replic, user)

    return replic.raw
