import pydantic
from pydantic import BaseModel
from typing import List, Union, Dict, Any, Optional
from enum import Enum
import logging
from bson.objectid import ObjectId
from json import JSONEncoder
import json

def _default(self, obj):
    return getattr(obj.__class__, "toJSON", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

class Id(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId) and not isinstance(v, str):
            raise TypeError('ObjectId required')
        try:
            print('validating..')
            res = Id(v)
            print(type(res))
            return res
        except bson.errors.InvalidId:
            logging.warning(f'{v} is not ObjectId')
            raise TypeError(f'{v} is not ObjectId')


    @classmethod
    def __modify_schema__(cls, schema):
        schema.update({
            'Title': 'MongoDB ObjectID',
            'type': 'string'
        })

    def toJSON(self):
        return str(self)

ObjectId.toJSON = Id.toJSON

class EntityType(str, Enum):
    """https://cloud.google.com/natural-language/docs/reference/rest/v1beta2/Entity#Type"""
    UNKNOWN = "UNKNOWN"
    PERSON = "PERSON"
    LOCATION = "LOCATION"
    ORGANIZATION = "ORGANIZATION"
    EVENT = "EVENT"
    WORK_OF_ART = "WORK_OF_ART"
    CONSUMER_GOOD = "CONSUMER_GOOD"
    OTHER = "OTHER"
    PHONE_NUMBER = "PHONE_NUMBER"
    ADDRESS = "ADDRESS"
    DATE = "DATE"
    NUMBER = "NUMBER"
    PRICE = "PRICE"

class Sentiment(BaseModel):
    score: float
    magnitude: float

class Entity(BaseModel):
    name: str
    type: EntityType
    meta: Dict[str, str]
    is_named: bool
    sentiment: Sentiment
    salience: float

class Token(BaseModel):
    raw: str
    offset: int # position in the original phrase
    pos: Dict[Any, Any] # Part of Speech; Make Enum

class Language(str, Enum):
    en = "en"
    other = "other"

class Category(BaseModel):
    """https://cloud.google.com/natural-language/docs/categories"""
    name: str
    confidence: float

class Speech(BaseModel):
    raw: str
    tokenized: List[Token]
    stylized: str
    args: List[Entity]
    sentiment: Union[Sentiment, None]
    categories: List[Category]
    lang: Language = Language.en

class Author(BaseModel):
    is_user: bool
    _id: str = ""

    class Config:
        extra = pydantic.Extra.allow

class Replic(BaseModel):
    user: Author
    author: Author
    timestamp: int
    speech: Speech
    _id: Optional[Id] = None

    class Config:
        extra = pydantic.Extra.allow

class SessionConfigs(BaseModel):
    local: bool = True
    visual: bool = False

class UserSettings(BaseModel):
    style: bool = False
    confirmation_threshold: float = 1.0

class UserState(BaseModel):
    dialog_skill_id: str = ""
    is_waiting: bool = False

class PublicUser(BaseModel):
    session: SessionConfigs = SessionConfigs()
    settings: UserSettings = UserSettings()
    state: UserState = UserState()

class User(PublicUser):
    token: Optional[str] = None
    _id: Optional[Id] = None
    telegram_id: Optional[int] = None

    class Config:
        extra = pydantic.Extra.allow

class Skill(BaseModel):
    url: str # b64
    author: Author
    name: str
    _id: Optional[Id] = None

    class Config:
        extra = pydantic.Extra.allow

class SkillInstance(BaseModel):
    skill: Skill
    local_state: str # b64
    global_state: str # b64
    user_id: Id
    _id: Optional[Id] = None

    class Config:
        extra = pydantic.Extra.allow
