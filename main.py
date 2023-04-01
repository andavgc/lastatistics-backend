import functions
import credentials
from api import *

user = 'ygtea'
r = credentials.lastfm_get('user.gettoptracks', user=user, period="6month", limit="10")
r = functions.get_data(r, user)
functions.create_json_file(r, "/home/andav/programacao/Projects/music-app/frontend/front/src/", "top_tracks")
