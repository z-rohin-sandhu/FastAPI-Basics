from fastapi import FastAPI
from src.config import Config
from src.routes import users, items, login
import os
import uvicorn
from webapps.routers import items as web_items, users as web_users, auth as web_auth
from fastapi.staticfiles import StaticFiles

ROOT_DIR = os.path.join(os.path.dirname(__file__),"./")
DOT_ENV_PATH = os.path.join(os.path.dirname(__file__),"./") + ".env"


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]  

app = FastAPI(title = Config.METADATA_DICT['TITLE'], 
              description = Config.METADATA_DICT['DESCRIPTION'], 
              version = Config.METADATA_DICT['VERSION'], 
              contact= {
                            "name" : Config.METADATA_DICT['NAME'],
                            "email": Config.METADATA_DICT['EMAIL']
                        },
              openapi_tags = tags_metadata, 
              openapi_url= Config.METADATA_DICT['OPENAPI_URL'], 
              redoc_url = Config.METADATA_DICT['REDOC_URL'], 
              docs_url = Config.METADATA_DICT['DOCS_URL']              
              )

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)
app.include_router(web_items.router)
app.include_router(web_users.router)
app.include_router(web_auth.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.UVICORN_DICT['host'], reload=Config.UVICORN_DICT['reload'], port=int(Config.UVICORN_DICT['port']))
