import requests
import json
import time
import os
import string
import logging
import nl_api
import utils
import flask
from kadia_common.types import Speech

def postprocess(text):
    tokens = utils.text2tokens(text)
    return Speech(tokens=tokens,
                  raw=text,
                  stylized=text,
                  args=[],
                  sentiment=None,
                  categories=[]
                  ).json()

def request_manager(request):
    print(request)
    request_json = request.get_json()
    text = request_json['text']
    if request.path == "/":
        return flask.jsonify(nl_api.annotate_text(text))
    else:
        return flask.jsonify(postprocess(text))
