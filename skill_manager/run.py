from fastapi import FastAPI, WebSocket, Body
from fastapi.responses import HTMLResponse
from schemes import *
import requests
import json
import time
import os
import string
import logging

app = FastAPI()

@app.post("/") # add more decorators
def reply(text: str = Body(..., embed=True)):
    do_truecase()
    do_ner()
    do_parse()
    speech = Speech(...)
    return speech.as_dict()
