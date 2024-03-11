#import fastapi
#import uvicorn
#import os
#from typing import List, Dict, Optional
#import numpy as np
#import orjson
#import schemas
import logging
#import asyncio
from fastapi import FastAPI, Request, HTTPException#, Header
from fastapi.responses import RedirectResponse
#import warnings
#from sqlalchemy.ext.asyncio import exc as sa_exc

# ------- global variables

_MODE = None
_INIT_CONFIG = None
_INIT_APP = None
WEB_PROTOCOL = None
WEBSITE_URL = None
MESSAGE_CONFLICT = None
MESSAGE_RETRY = None
URL_KEY_RETRY = 0

# ------- Logging format

#FMTSTR="[%(asctime)s] %(levelname)-8s: %(funcName)-16s: %(module)-12s: %(message)s"
FMTSTR="[%(asctime)s] %(levelname)-8s<~> %(funcName)-16s<~> %(message)s"
#DTSTR="%Y/%m/%d %H:%M:%S %z"
#logging.Formatter.converter = time.gmtime # Note: convert time to GMT
DTSTR="%Y/%m/%d %H:%M:%SZ"

# ------- Execption

async def not_found_error(request: Request, exc: HTTPException):
    #print(exc.args, exc.detail, exc.status_code)
    return RedirectResponse('/404')

exception_handlers = {404: not_found_error}

app = FastAPI(exception_handlers=exception_handlers) # Note: cant take __name__ as argument
app.config = dict()
app.register_blueprint = app.include_router 

#WEBSITE_URL = "lnkk.in:8000"
#app.config['SERVER_NAME'] = WEBSITE_URL

# ------- Common APIs

@app.get("/health", status_code=200)
async def health():
    return "ok"

@app.get("/404",status_code=404)
async def not_found():
    return HTTPException(status_code=404, detail="Not Found!")

# ------- Middleware
    
class ASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            #print(scope.keys())
            # ------- extracting request host name
            #host = [_[1].decode() for _ in scope['headers'] if _[0]==b'host'][0]
            # OR
            host = ""
            for header in scope['headers']:
                if header[0]==b'host':
                    host = header[1].decode()
                    break
                #else:
                #    continue
            # ------- fetching subdomain out of host name
            subdomain = host.replace(f".{app.config['SERVER_NAME']}","")
            #print("Host: ", host, subdomain)
            # ------- adding custom http header
            scope['headers'].append((b'tenant', subdomain.encode()))
            ##import pdb;pdb.set_trace()
            ##print(scope.keys())
            ##self.subdomain = subdomain
        await self.app(scope, receive, send)

"""
@app.midleware("http")
async def add_process_time_header(request: Request, call_next):
    host = request.headers.get("host")
    subdomain = request.headers.get("tenant")
    print("Host: ", host, subdomain) # PS: tenant info would not be there
    response = await call_next(request)
    return response
"""

# ------- warnings

# with warnings.catch_warnings():
#     warnings.simplefilter("ignore", category=sa_exc.exc.SAWarning)

"""
# ------- routes

@app.get("/ping2")
async def ping2():
    logging.info("pinging.....")
    logging.warning("pinging.....")
    return "pong"

@app.get("/")
def index():
    return {"message":"Welcome to FastAPI[all]", "version": fastapi.__version__}

@app.get("/ping")
def ping(request: Request):
    print(request.headers.get('tenant'))
    return "pong"

@app.get("/test/{nunber:int}")
def id(nunber: int, id: Optional[int] = None) -> Dict:
#def id(id: int|None = None) -> List: # Note: from python 3.10 only
    #print(f"***\t{type(id)}\t***")
    return {"id":id, "nunber":nunber} 

@app.get("/not_found/{id}")
def not_found(id: int):
   temp_d = {1:"k", 2:"ok", 3:"oki", 4:"okay"}
   if temp_d.get(id):
       return temp_d[id]
   raise HTTPException(detail=f'id:{id} not found', status_code=404)
   #return HTTPException(detail=f'id:{id} not found', status_code=404)

@app.post("/categories/")
#def insert_categories(request: dict):
def insert_categories(request : schemas.CategoriesPayload):
    #print("***", type(request), CategoriesPayload(**request))
    #return {"category_name":request.category_name,\
    #        "category_description":request.category_description}
    from models import Categories
    from database import SQLClass
    sql = SQLClass()
    #import pdb;
    #pdb.set_trace();
    #categories = [_.dict() for _ in request.categories]
    # OR using pydantic json
    categories = orjson.loads(request.json())['categories']
    # OR
    # np array implementation (vectorization)
    #arr = np.array(request.categories)
    #categories = np.apply_along_axis(lambda l: list(map(lambda idx: l[idx].dict(), range(len(l)))), axis=0, arr=arr).tolist()
    sql.insert_into_table_using_session(Categories,*categories)
    return request.categories

"""

# swagger URL:
#http://127.0.0.1:8000/docs
#http://127.0.0.1:8000/redoc
# JSON API
#http://127.0.0.1:8000/openapi.json

def create_app(test_config=None): # create_app is specific for Flask
    from setup.sql import init_sql
    from config import get_config
    from controller import UserBlueprint, PostBlueprint
    global _INIT_APP, WEBSITE_URL, _MODE, WEB_PROTOCOL, MESSAGE_CONFLICT, URL_KEY_RETRY, MESSAGE_RETRY, app

    if _INIT_APP:
        return _INIT_APP
    # ------- Middleware
    app.add_middleware(ASGIMiddleware)
    # ------- getting configuration
    config = get_config()
    # domain config
    WEBSITE_URL = config['common']['website_url']
    app.config['SERVER_NAME'] = WEBSITE_URL
    _MODE = config['common']['mode']
    WEB_PROTOCOL = config[_MODE]['web_protocol']
    # other config
    MESSAGE_CONFLICT = config['common']['message_conflict']
    MESSAGE_RETRY = config['common']['message_retry']
    URL_KEY_RETRY = config['common'].getint("url_key_retry")
    # ------- initializing RDBMS
    #app = init_sql(app, config, engine_name="postgres")
    init_sql(app, config, engine_name="postgres")
    # ------ registering Blueprints
    app.register_blueprint(UserBlueprint)
    app.register_blueprint(PostBlueprint)
    # ------ setting LOGGING
    logging.basicConfig(filename="/tmp/fastapi-output.log", filemode="a", format=FMTSTR, datefmt=DTSTR, level=logging.WARNING)
    _INIT_APP = app
    return app

app = create_app()
"""
if __name__ == "__main__":
    #uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True) # Note: app.run() does't exist 
    #uvicorn.run('app:app', host="0.0.0.0", port=8000, workers=4) 
    #uvicorn app:app --reload
    '''--workers INTEGER Number of worker processes. Defaults to the $WEB_CONCURRENCY environment variable if available, or 1. Not valid with --reload'''
    #uvicorn app:app --workers 4
    #uvicorn --factory "fastapi-app:create_app" --workers 4 --host "0.0.0.0" --port 8080 --log-level 'warning' --no-access-log
    #gunicorn "app:create_app()" --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker --error-logfile guni_error_fastapi.log
    #
    # python app.py
    # Note: don't forget to set local env variables through below command(for linux)
    # export DB_NAME="testdb" DB_PORT="3307" DB_PASSWORD="12345678"

"""