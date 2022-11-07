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

def get_cinestream_json(): 
    movies_dict = {}
    movies_file = open('movies_CineStream.json')
    movies_dict = json.load(movies_file)
    movies_file.close()
    return json.dumps(movies_dict)

@app.get("/cine_movies")
def read_root():
    movies_list = get_cinestream_json()
    #movies_list = get_videos_cinestream()
    return Response(content=movies_list, media_type="application/json") 

"""get_routes()
app = VersionedFastAPI(app, version_format='{major}',prefix_format='/v{major}')
app.include_router(router)"""