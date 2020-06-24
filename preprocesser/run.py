from fastapi import FastAPI, WebSocket, Body
from fastapi.responses import HTMLResponse
from schemes import *
import requests
import json
import time
import os
import string
import logging

mask = '[MASK]'
digits = "0123456789"
punctuation = string.punctuation + '’“”’—‘' + '–'

"""
Useful links:

!!!Dataset instructions: https://www.weak-learner.com/blog/2019/12/27/ontonotes-5/
!!!Training instruction: https://huggingface.co/transformers/v2.2.0/examples.html#training

DeepPavlov configs: https://github.com/deepmipt/DeepPavlov/blob/master/deeppavlov/configs/ner/ner_ontonotes_bert.json
Example: https://github.com/flairNLP/flair
"""

def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI

def parse_to_words(text):
    text = text.lower()
    words = []
    words_indexes = []
    current = []
    for i, el in enumerate(text + ' '):
        if el.isalpha():
            current.append(el)
        elif el in digits:
            if len(current) != 0 and not current[-1] in digits:
                words.append(''.join(current))
                words_indexes.append([i - len(current), i - 1])
                current = []
            current.append(el)
        elif el.isspace():
            if len(current) != 0:
                words.append(''.join(current))
                words_indexes.append([i - len(current), i - 1])
                current = []
        elif el in punctuation: # commas, dots, slashes
            if len(current) != 0:
                words.append(''.join(current))
                words_indexes.append([i - len(current), i - 1])
                current = []
            words.append(el)
            words_indexes.append([i, i])
        elif char_is_emoji(el): # emoji
            words.append('[UNK]')
            words_indexes.append([i, i])
        else:
            logging.warning(f"Warning! Strange char {el}")
    return words, words_indexes

def do_truecase(text):
    """
    truecase text https://pypi.org/project/truecase/
    source: https://arxiv.org/pdf/1903.11222.pdf
    """
    pass

def do_ner(text):
    """use distilbert-base-cased"""
    pass

def do_parse(text, entities):
    """parse text to tokens. Entity must be a single token"""
    pass

app = FastAPI()

@app.post("/") # add more decorators
def reply(text: str = Body(..., embed=True)):
    do_truecase()
    do_ner()
    do_parse()
    speech = Speech(...)
    return speech.as_dict()

@app.post("/postprocess") # add more decorators
def reply(text: str = Body(..., embed=True)):
    do_parse()
    speech = Speech(...)
    return speech.as_dict()
