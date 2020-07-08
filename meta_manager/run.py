from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from kadia_common.types import *
from kadia_common.db import MongoDB, SkillNotFound
import requests
import json
import time
import os
from typing import Dict, Any

PREPROCESSOR_URL = os.getenv("PREPROCESSER_URL")
SKILL_MANAGER_URL = os.getenv("SKILL_MANAGER_URL")

MONGO_URL = os.getenv("MONGO_URL")
db = MongoDB(MONGO_URL)

TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = FastAPI()

@app.post("/telegram/{token}") # add more decorators
def process_telegram(token: str, message: Dict[Any, Any] = Body(..., embed=True)):
    assert(token == TOKEN)
    user_id = message['from']['id']
    text = message['text']
    user = db.fetch_telegram_user(user_id)
    response = reply(user, text)
    requests.post(TELEGRAM_URL, json={
        'chat_id': message['chat']['id'],
        'text': response
    })
    return {'ok': True}

def make_replic(speech, user, author):
    return Replic(
        speech=speech,
        user=user,
        author=author,
        timestamp=time.time(), # make timezone agnostic
    )


def reply(user, text):
    if user.state.dialog_skill_id == "" and "/run" not in text:
            return "Sorry, I do not understand you. Use /run to start dialog"
    skill_id = user.state.dialog_skill_id
    if "/run" in text:
        parts = text.split()
        skill_id = parts[1]
        text = ' '.join(parts[2:])

    try:
        response = requests.post(PREPROCESSOR_URL, json={"text": text})
        print(response.status_code, response.text, text)
        response.raise_for_status()
        if response.status_code == 400:
            return "oops2"
    except:
        return "oops"
    skill_id = Id(skill_id)
    print(response.status_code, response.text, text)
    speech = Speech(**response.json())
    replic = make_replic(author=Author(is_user=True, _id=user._id), # user._id
                        user=Author(is_user=True, _id=user._id),
                        speech=speech)
    db.add_replic_to_history(replic)
    db.change_user_waiting_status(user, True)

    try:
        skill = db.fetch_skill(skill_id)
    except SkillNotFound as exc:
        return str(exc)
    print('skill', skill.dict(), type(skill._id))
    print(type(Id(skill._id)))
    json.dumps(skill.dict())
    print('user', user.dict(), type(user._id))
    json.dumps(user.dict())
    print('speech', speech.dict())
    json.dumps(speech.dict())

    resp = requests.post(SKILL_MANAGER_URL, json={'skill': skill.dict(),
                                                  'user': user.dict(),
                                                  'speech': speech.dict()})
    print(resp, resp.text)
    if resp.status_code != 200:
        return "Oops, something went wrong..."
    resp.raise_for_status()
    resp = resp.json()

    db.change_user_waiting_status(user, False)

    replic = make_replic(user=Author(is_user=True, _id=user._id),
                        author=Author(is_user=False, _id=skill_id),
                        speech=Speech(**resp['speech']))
    db.add_replic_to_history(replic)

    return replic.speech.raw
