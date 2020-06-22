from fastapi import FastAPI, WebSocket, Body
from fastapi.responses import HTMLResponse
from schemes import *

app = FastAPI()

def load_data(data):
    pass

def recursive_split(speech, candidates):
    pass

def save_data():
    return "b64string"

def ask_

@app.post('/')
def recognize_algo(user: User = Body(..., embed=True), \
                   speech: Speech = Body(..., embed=True),
                   data: str = Body("", embed=True)):
    load_data(data)
    candidates = []
    recursive_split(speech, candidates)
    phrases2score = dict()
    best_id = 0
    best_score = 0
    for i, el in enumerate(candidates):
        pass
    save_data()
    pass
