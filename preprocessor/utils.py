import json
import time
import os
import string
import logging
from kadia_common.types import Token

mask = '[MASK]'
digits = "0123456789"
punctuation = string.punctuation + '’“”’—‘' + '–'


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

def text2tokens(text):
    words, words_indexes = parse_to_words(text)
    tokens = []
    for i in range(len(words)):
        token = Token(raw=words[i],
                      offset=words_indexes[i][0],
                      pos={})
    return tokens
