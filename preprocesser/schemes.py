from pydantic import BaseModel
from typing import List

class Tag(BaseModel):
    tag: str
    score: float

class Token(BaseModel):
    tags: List[Tag]
    raw: str
    ind: int # position in the original phrase

class Speech(BaseModel):
    raw: str
    tokenized: List[Token]
    stylized: str
    args: List[Token]

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
    script_skill_id: str = ""

class PublicUser(BaseModel):
    session: SessionConfigs = SessionConfigs()
    settings: UserSettings = UserSettings()
    state: UserState = UserState()

class User(PublicUser):
    token: str
