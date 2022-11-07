import requests 
import json
from fastapi import FastAPI, Response, APIRouter
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI()

router = APIRouter()
all_routes =[]

def get_routes():
    reserved_routes = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]
    for route in app.routes:
        if route.path not in reserved_routes:
            if route.name is not None:
                version = getattr(route.endpoint, "_api_version", (2, 0))
                all_routes.append("/v" + str(version[0]) + route.path)

def get_all_movies(): 
    all_movies_dict = {}
    try: 
        cinestream_movie_response = requests.get("http://localhost:8004/cine_movies")
        cinestream_movies = json.loads(cinestream_movie_response.content.decode('utf8'))
        all_movies_dict.update(cinestream_movies)
    except: 
        print("CINESTREAM NA")
    try: 
        netflix_movies_response = requests.get("http://localhost:8003/netflix_movies")
        netflix_movies = json.loads(netflix_movies_response.content.decode('utf8'))
        all_movies_dict.update(netflix_movies)
    except: 
        print("NETFLIX NA")
    try: 
        prime_movies_response = requests.get("http://localhost:8002/prime_movies")
        prime_movies = json.loads(prime_movies_response.content.decode('utf8'))
        all_movies_dict.update(prime_movies)
    except: 
        print("PRIME NA")
    all_movies_json = json.dumps(all_movies_dict, indent = 4) 
    return all_movies_json


@app.get("/All_OTT")
async def read_root():
    all_movies_json = get_all_movies()
    return Response(content=all_movies_json, media_type="application/json")

"""get_routes()
app = VersionedFastAPI(app, version_format='{major}',prefix_format='/v{major}')
app.include_router(router)"""