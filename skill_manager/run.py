from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
import requests
import json
import time
import os
import string
import logging
from kadia_common.types import *
from kadia_common.db import MongoDB
import shutil
import json

app = FastAPI()

secret_params = json.load(open('secrets.json'))
db = MongoDB(secret_params['mongo_url'])

def install_skill(skill: Skill):
    os.system(f'git clone {skill.url} /skill')

def clean_skill():
    shutil.rmtree('/skill')
    os.mkdir('/skill')

def run_skill(instance: SkillInstance, user: User, speech: Speech):
    with open('/skill/local_state.b64', 'w') as file:
        print(instance.local_state, file=file)
    with open('/skill/global_state.b64', 'w') as file:
        print(instance.global_state, file=file)
    with open('/skill/user.json', 'w') as file:
        json.dump(user.dict(), file) # PublicUser ?
    with open('/skill/speech.json', 'w') as file:
        json.dump(speech.dict(), file)

    assert(os.system('firejail bash') == 0)
    assert(os.system('python -c "import json"') == 0)
    print('code', os.system(f'cd /skill && firejail python run.py'))
    # --timeout=00:00:{10}
    try:
        print('logs', open('/skill/logs.txt').read())
        print('out', open('/skill/out.txt').read())
    except Exception as exp:
        print(exp)
    print(os.listdir('/skill'))
    try:
        local_state = open('/skill/local_state.b64').read()
    except:
        local_state = ""

    try:
        global_state = open('/skill/global_state.b64').read()
    except:
        global_state = instance.global_state

    try:
        output = open('/skill/output.txt').read()
    except Exception as exp:
        print(exp)
        output = "Something went wrong."

    return output, local_state, global_state

@app.post("/") # add more decorators
def reply(skill: Skill = Body(..., embed=True),
          user: User = Body(..., embed=True),
          speech: Speech = Body(..., embed=True)):
    print(skill.dict())
    print(user.dict())
    print(speech.dict())
    install_skill(skill)
    print('vvvvvv')
    instance = db.fetch_skill_instance(skill=skill, user=user)
    print('rrrrr')
    output, local_state, global_state = run_skill(instance, user, speech)
    print('qqqqq')
    db.update_instance(instance, local_state, global_state)
    print('output', output)
    resp = requests.post(secret_params['processor_url'], json={"text": output})
    print(resp, resp.text, flush=True)
    speech = Speech(**resp.json())
    clean_skill()
    return {'speech': speech.dict()}
