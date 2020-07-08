import pymongo
from kadia_common.types import *
from kadia_common.db import MongoDB
import os
url = os.getenv('MONGO_URL')
print(url)
db = MongoDB(url)

skill = {
    'url': 'https://github.com/Kadia-IVA/echo-skill',
    'author': {
        'is_user': True,
        '_id': ""
    },
    'name': 'echo'
}

print('...')
skill = Skill(**skill)
try:
    print(db.add_skill(skill))
except:
    db._remove_skill(name=skill.name)
    print('skill removed')
    exit(0)
