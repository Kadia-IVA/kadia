from pydantic import BaseModel
from typing import List

class Tag(BaseModel):
    tag: str # Make Enum
    score: float

class Token(BaseModel):
    tags: List[Tag]
    raw: str
    ind: int # position in the original phrase
    pos: str # Part of Speech; Make Enum

class Speech(BaseModel):
    raw: str
    tokenized: List[Token]
    stylized: str
    args: List[Token]
    sentoment: float # from -1 to 1. It is not supported for now.

class Author(BaseModel):
    is_user: bool
    _id: str

class Replic(BaseModel):
    author: Author
    timestamp: int
    speech: Speech

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
    token: str

class Skill(BaseModel):
    zip: str # b64
    author: Author
    name: str

class SkillInstance(BaseModel):
    skill: Skill
    state: str # b64
    user_id: str
