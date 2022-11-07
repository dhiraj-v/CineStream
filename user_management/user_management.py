import json 
from fastapi import FastAPI, HTTPException, APIRouter
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

@app.get("/userauth/{email}")
def user_auth(email: str):
    user_dbfile = open('user_details.json')
    users_dict = json.load(user_dbfile)
    user_dbfile.close()
    emails = []
    for user in users_dict["users"]:
        print(user["email"]) 
        if user["email"] == email:
            uid = user["uid"]
            return f"{uid}"
    return HTTPException(status_code=404, detail=f"user with {email} does not exist")

"""get_routes()
app = VersionedFastAPI(app, version_format='{major}',prefix_format='/v{major}')
app.include_router(router)
"""