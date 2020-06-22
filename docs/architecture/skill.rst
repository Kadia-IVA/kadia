Skill
====================

Skill is the exterior module of Kadia. There are 2 types of skills: conversations and scripts.
Scripts can be embedded in conversations, but can not interact with the user.
Conversations are skills that consecutively interacts with the user.

Skill is running only when processing the request.

Skill response may be one of these:
- text (not an option for scripts)
- i do not understand you flag
- text with the end of dialog flag
