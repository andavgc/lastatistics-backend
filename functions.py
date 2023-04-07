import json

import requests
import credentials
from bs4 import BeautifulSoup

def get_data(json_obj, user, period, limit):
    
    music_list = []
    
    if list(json_obj.keys())[0] == "topalbums":
        albums = json_obj["topalbums"]["album"]

        for item in albums:
            
            album = {
                "name": item["name"],
                "artist": item["artist"]["name"],
                "rank": item["@attr"]["rank"],
                "cover": item["image"][-1]["#text"],
                "playcount": item["playcount"]
            }
            
            music_list.append(album)
    
    elif list(json_obj.keys())[0] == "topartists":
        artists = json_obj["topartists"]["artist"]
        
        for item in artists:
            
            url = item["url"]
            
            artist = {
                "name": item["name"],
                "rank": item["@attr"]["rank"],
                "cover": item["image"][-1]["#text"],
                "playcount": item["playcount"]
            }

            # try:
            artist = get_artist_img(url, artist)
            # except:
            #     pass
            music_list.append(artist)
    
    elif list(json_obj.keys())[0] == "toptracks":
        tracks = json_obj["toptracks"]["track"]

        for item in tracks:
            
            track = {
                "name": item["name"],
                "artist": item["artist"]["name"],
                "rank": item["@attr"]["rank"],
                "cover": item["image"][-1]["#text"],
                "playcount": item["playcount"]
            }
            
            try:
                track = get_track_album(track)
            except:
                pass         
            music_list.append(track)

    music_obj = {
        'user':user,
        'period': period,
        'length': limit,
        'infolist':music_list
    }
    return music_obj
    
def get_track_album(track_obj):

    json_obj = credentials.lastfm_get('track.getinfo', track=track_obj["name"], artist=track_obj["artist"])

    if "album" in json_obj["track"]:
        track_obj["album"] = json_obj["track"]["album"]["title"]
        track_obj["cover"] = json_obj["track"]["album"]["image"][-1]["#text"]
    else:
        track_obj["album"] = track_obj["name"]
        track_obj["cover"] = track_obj["cover"]
    return track_obj

def get_artist_img(url, artist_obj):

    #getting artist gallery url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    anchor = soup.find('a', class_="header-new-gallery header-new-gallery--link hidden-xs link-block-target")
    gallery_url = "https://www.last.fm" + anchor['href']

    #getting url for the first image in gallery
    r = requests.get(gallery_url)
    soup = BeautifulSoup(r.content, 'lxml')
    img_source = soup.find('img', class_="js-gallery-image")
    artist_obj["cover"] = img_source["src"]

    return artist_obj

def create_json_file(obj, path, name):
    result = json.dumps(obj, sort_keys=True, indent=4)
    if path[-1] == "/":
        jsonFile = open(path + name + ".json", "w")
    else:
        jsonFile = open(path + "/" + name + ".json", "w")
    jsonFile.write(result)
    jsonFile.close()
