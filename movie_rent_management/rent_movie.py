import requests
import json
from fastapi import FastAPI, Response, APIRouter
from fastapi_versioning import VersionedFastAPI, version

from pydantic import BaseModel

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


@router.get("/")
def index():
    return { "endpoints": all_routes }


class RentAMovie(BaseModel):
    movieid: str
    userid: int

def get_movies_for_rent(): 
    rent_movies_dict = {}
    try: 
        netflix_movies_response = requests.get("http://localhost:8003/netflix_movies")
        netflix_movies = json.loads(netflix_movies_response.content.decode('utf8'))
        rent_movies_dict.update(netflix_movies)
    except: 
        print("NETFLIX NA")
    try: 
        prime_movies_response = requests.get("http://localhost:8002/prime_movies")
        prime_movies = json.loads(prime_movies_response.content.decode('utf8'))
        print(prime_movies)
        rent_movies_dict.update(prime_movies)
    except: 
        print("PRIME NA")
    rent_movies_json = json.dumps(rent_movies_dict, indent = 4) 
    print(rent_movies_json)
    return rent_movies_json

@app.post("/rent_a_movie/")
async def rent_a_movie(rentmovie: RentAMovie): 
    rent_json_data = json.load(open("rent.json")) 
    new_rent_dict = {}
    if (json.loads(requests.get("http://localhost:8008/payment/?payment_details=true").content.decode('utf8'))["message"]) == "success": 
        new_rent_dict["uid"] = rentmovie.userid
        new_rent_dict["mid"] = rentmovie.movieid
        new_rent_dict["validity"] = True
        rent_json_data['rents'].append(new_rent_dict)
        with open('rent.json', 'w') as f:
            json.dump(rent_json_data, f)
        print()
        return {"message": "Movie Rented"}
    return {"message": "no money no rent"}

@app.put("/retire_rent/")
async def delete_expired_movies():
    rent_json_data = json.load(open("rent.json"))
    print(rent_json_data)
    for element in rent_json_data["rents"]: 
        if element["validity"] == True: 
            element["validity"] = False
    with open('rent.json', 'w') as f:
        json.dump(rent_json_data, f)

@app.get("/test/")
def test_payment(): 
    var = requests.get("http://localhost:8000/payment/?payment_details=false")
    print(var)

"""get_routes()
app = VersionedFastAPI(app, version_format='{major}',prefix_format='/v{major}')
app.include_router(router)"""