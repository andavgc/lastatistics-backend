from bson import ObjectId
from fastapi import Query
from pydantic import BaseModel
from typing import List, Optional

class Track(BaseModel):
    album: str
    artist: str
    cover: str
    name: str
    playcount: str
    rank: str
    
class User(BaseModel):
    user: str
    period: str
    length: str
    tracklist: List[Track]

class newUser(BaseModel):
    user: str
    period: str
    limit: str
