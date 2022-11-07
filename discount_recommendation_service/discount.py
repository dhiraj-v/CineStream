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

class Discount(BaseModel): 
    userid: int 

@app.get("/get_discounts/")
def get_discount(): 
    discount_json = json.dumps(json.load(open("discounts.json")))
    return Response(content=discount_json, media_type="application/json") 

@app.post("/update_discounts/")
async def update_discounts(discount: Discount): 
    user_activity_json = requests.get("http://localhost:8001/get_activity")
    user_activity_dict = json.loads(user_activity_json.content.decode('utf8'))
    for element in user_activity_dict["activity"]: 
        if element["uid"] == discount.userid: 
            return {"message": f"{discount.userid} can avail Discount"}
        else: 
            return {"message": f"{discount.userid} needs to participate more"}

"""get_routes()
app = VersionedFastAPI(app, version_format='{major}',prefix_format='/v{major}')
app.include_router(router)"""