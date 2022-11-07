from fastapi import FastAPI, APIRouter
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

@app.get("/payment/")
def payment_success(payment_details: bool):
    if payment_details == True: 
        return {"message": "success"} 
    else: 
        return {"message": "failed"}

"""get_routes()
app = VersionedFastAPI(app, version_format='{major}',prefix_format='/v{major}')
app.include_router(router)"""