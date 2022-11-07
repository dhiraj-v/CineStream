import requests 
import json
from fastapi import FastAPI, Response

def get_all_movies(): 
    all_movies_dict = {}
    try: 
        cinestream_movie_response = requests.get("http://localhost:8001/cine_movies")
        cinestream_movies = json.loads(cinestream_movie_response.content.decode('utf8'))
        all_movies_dict.update(cinestream_movies)
    except: 
        print("CINESTREAM NA")
    try: 
        netflix_movies_response = requests.get("http://localhost:8002/netflix_movies")
        netflix_movies = json.loads(netflix_movies_response.content.decode('utf8'))
        all_movies_dict.update(netflix_movies)
    except: 
        print("NETFLIX NA")
    try: 
        prime_movies_response = requests.get("http://localhost:8003/prime_movies")
        prime_movies = json.loads(prime_movies_response.content.decode('utf8'))
        all_movies_dict.update(prime_movies)
    except: 
        print("PRIME NA")
    all_movies_json = json.dumps(all_movies_dict, indent = 4) 
    print(all_movies_json)

get_all_movies()

