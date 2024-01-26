from dotenv import load_dotenv, find_dotenv
import os
import base64
from requests import post,get,put
import json
from speechtotext import *

#path="C:\Users\krish\OneDrive\Desktop\Project 1 Virtual Assistant\Spotify API"
BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(find_dotenv())

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") 
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers= headers,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers= get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("Artist not found.")
        return None
    return json_result[0]

def search_for_track(token,track_name):
    url = "https://api.spotify.com/v1/search"
    headers= get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"
    
    query_url = url + query
    
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("song not found.")
        return None
    return json_result[0]

def get_device_id(token):
    url = "https://api.spotify.com/v1/me/player/devices"
    headers=get_auth_header(token)
    result = get(url,headers=headers)
    json_result=json.loads(result.content)
    return json_result

def get_songs_by_artist(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers= get_auth_header(token)
    result = get(url,headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def play_song(token,name):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = get_auth_header(token)
    uri = search_for_track(token,name)['uri']
    print(uri)
    data = {
        "uris" : [f"{uri}"]
    }
    result = put(url,data=json.dumps(data),headers=headers)
    print(result.status_code)
    
token = get_token()
result = search_for_artist(token, "J Cole")
# print(result["followers"]["total"])
artist_id = result["id"]
songs = get_songs_by_artist(token,artist_id)

# play_song(token)
# for idx,song in enumerate(songs):
#     print(f"{idx+1}. {song['name']}")
    
# res=search_for_track(token,"No Role Modelz")
# print(res["uri"])

# res=get_device_id(token)
# print(res)

def get_song_from_user(inp):
    inp=inp.split()
    song=""
    for i in range(inp.index("play")+1,inp.index("by")):
        song+=inp[i]
    return song

refreshtoken = os.getenv("REFRESH_TOKEN")

def refresh_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": "AQA4zsLFSQPD6VjfTxLGgnagyyDKX8lKVSJtWBwnjJPSyb_nolzr7jmelaCbA6DnPxAp8NHSzDndZxAxetWo9nqjZLS3cs-YK4t-ZnQunzyLj7sC_tD9p2Z2B_EqHorXmpg"
    }
    response = post(url, headers=headers, data=data)
    # json_result = json.loads(response.content)
    # print(json_result)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Failed to refresh token:", response.status_code)
        return None




def main():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    token = refresh_token(client_id,client_secret)
    ip = speechrecog()
    print(ip)
    print(get_song_from_user(ip.lower()))
    play_song(token,get_song_from_user(ip.lower()))
    print(search_for_track(token,get_song_from_user(ip.lower()))['uri'])
    
if __name__ == '__main__':
    main()
# ip = speechrecog()
# print(ip)
# print(get_song_from_user(ip.lower()))
# tokennew='BQBhldlCks6nd0JmFqop_BIn0N8DBFYSZfO20KOzGvENIIly0170RLtIUV0yy6UsO2Z5j70DJaLVwIAryIsFJ6iMgJRB0RpJlWSJWEJcr6OJvbAlt_Mlr71rxmqH70OMMRifqA0IBwEY1kynLEuD-8PH3yx2XMM0kJJGZzj4krYLcVX9Y4iL_hKL9DWYZPxZ3XYUDACzIzqp8C9tojQH3D-wjJzVaAsGrcB8MwwZqFwfGKp7HQZkP9TKldC9k3TS0iid5L--TJVloo5ycgnSJM-_iXBR'
# play_song(tokennew,get_song_from_user(ip.lower()))
# print(search_for_track(token,get_song_from_user(ip.lower()))['uri'])
