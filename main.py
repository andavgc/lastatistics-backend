from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import User, newUser
from typing import List
import credentials
import functions
from database import (
    fetch_user,
    fetch_all_users,
    create_user,
    update_user
    )

app = FastAPI()

# origins = 'http://localhost:8000/'

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials = True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

def get_user_info(info_tpye, user:newUser):
    r = credentials.lastfm_get(info_tpye, user=user.user, period=user.period, limit=user.limit)
    document = functions.get_data(r, user.user, user.period, user.limit)
    return document

@app.get("/")
def read_root():
    return {"music-app_api": "working"}

@app.get("/api/music-info")
async def get_info():
    response = await fetch_all_users()
    return response

@app.get("/api/music-info/{user}", response_model=User)
async def get_user(user):
    response = await fetch_user(user)
    
    if response:
        return response
    raise HTTPException(404, f"{user} not found")

@app.post("/api/music-info", response_model=User)
async def post_tracklist(user:newUser):
    limit = "10"
    print(user)
    document = get_user_info('user.gettoptracks', user)
    response = await create_user(document)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")

@app.put("/api/music-info", response_model=User)
async def put_tracklist(user:newUser):
    document = get_user_info('user.gettoptracks', user)
    response = await update_user(document)
    if response:
        return response
    raise HTTPException(404, f"{user} not found")
