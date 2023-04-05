from dotenv import load_dotenv
import os
from requests import get

# authentication

#getting data for authentication from .env file
load_dotenv()
client_id = os.getenv("API_KEY_LASTFM")
client_secret = os.getenv("SHARED_SECRET_LASTFM")

def lastfm_get(method, user=None, period="overall", limit="50", page="1", track=None, artist=None):
    # define headers and URL
    headers = {'user-agent': "andres"}
    url = "https://ws.audioscrobbler.com/2.0/"
    payload = {}

    # Add API key and format to the payload
    payload['api_key'] = client_id
    payload['format'] = 'json'
    payload['method'] = method

    if 'user.' in method:
        payload['user'] = user
    elif 'track.' in method:
        payload['track'] = track
        payload['artist'] = artist
    if period:
        payload['period'] = period
    if limit:
        payload['limit'] = limit
    if page:
        payload['page'] = page

    response = get(url, headers=headers, params=payload)
    response = response.json()
    return response
