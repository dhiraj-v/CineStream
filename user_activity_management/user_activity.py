from fastapi import FastAPI, Response, APIRouter
from fastapi_versioning import VersionedFastAPI, version
from pydantic import BaseModel
import json
import requests

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

class Activity(BaseModel): 
    userid: int 
    movieid: str 
    rating: int

@app.post("/activity_update/")
async def update_activity(user_activity: Activity):
    activity_json_data = json.load(open("activity.json")) 
    new_activity_dict = {}
    new_activity_dict["uid"] = user_activity.userid
    new_activity_dict["mid"] = user_activity.movieid
    new_activity_dict["rating"] = user_activity.rating
    activity_json_data['activity'].append(new_activity_dict)
    with open('activity.json', 'w') as f:
        json.dump(activity_json_data, f)
    return {"message": "activity Logged"}

@app.get("/get_activity/")
def get_activity(): 
    activity_json_data = json.load(open("activity.json"))
    return Response(content=json.dumps(activity_json_data), media_type="application/json")

"""get_routes()
app = VersionedFastAPI(app, version_format='{major}',prefix_format='/v{major}')
app.include_router(router)"""