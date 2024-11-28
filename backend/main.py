from pymongo import MongoClient
import dotenv
import os
import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

dotenv.load_dotenv()

URI = "mongodb+srv://codingtathya:{db_password}@lang-v-lang.xijyg.mongodb.net/?retryWrites=true&w=majority&appName=lang-v-lang"
DB_PASSOWRD = os.getenv('PASSWORD')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"]
)

class Update(BaseModel):
    language: str
    update_by: int
    group: str

@app.get('/')
async def root():
    return {"message": "hello, world!"}


@app.get('/fetch')
async def fetch_language_votes(language: str):
    try:
        client = MongoClient(URI.format(db_password=DB_PASSOWRD))
        database = client["votes"]
        langs = database["languages"]

        votes = langs.find_one({'name': language})['votes']

        client.close()

        return {'status': 200, 'votes': votes}
    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)


@app.put('/update')
async def update_language_votes(update_data: Update):
    try:
        client = MongoClient(URI.format(db_password=DB_PASSOWRD))
        database = client["votes"]
        langs = database["languages"]
        groups = database["groups"]

        lang_votes = langs.find_one({'name': update_data.language})['votes']
        langs.update_one({'name': update_data.language}, {'$set': {'votes': lang_votes + update_data.update_by}})

        group = groups.find_one({'name': update_data.group})
        print(group, update_data.group)
        if group:
            group_votes: int = group['votes']
            groups.update_one({'name': update_data.group}, {'$set': {'votes': group_votes + update_data.update_by}})
        else:
            groups.insert_one({'name': update_data.group, 'votes': update_data.update_by})

        client.close()

        return {'status': 200}
    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)


@app.get('/fetch-group')
async def fetch_group(group_name: str):
    try:
        client = MongoClient(URI.format(db_password=DB_PASSOWRD))
        database = client["votes"]
        groups = database["groups"]

        group = groups.find_one({'name': group_name})
        group_votes: int = group['votes']

        client.close()

        return {'status': 200, 'votes': group_votes}
    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)


