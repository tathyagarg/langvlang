from pymongo import MongoClient
import dotenv
import os
import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

URI = "mongodb+srv://codingtathya:{db_password}@lang-v-lang.xijyg.mongodb.net/?retryWrites=true&w=majority&appName=lang-v-lang"
DB_PASSOWRD = os.getenv('PASSWORD')

app = FastAPI()

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
async def update_language_votes(language: str, update_by: int, group_name: str):
    try:
        client = MongoClient(URI.format(db_password=DB_PASSOWRD))
        database = client["votes"]
        langs = database["languages"]
        groups = database["groups"]

        lang_votes = langs.find_one({'name': language})['votes']
        langs.update_one({'name': language}, {'$set': {'votes': lang_votes + update_by}})

        group = groups.find_one({'name': group_name})
        if group:
            group_votes: int = group['votes']
            groups.update_one({'name': group}, {'$set': {'votes': group_votes + update_by}})
        else:
            groups.insert_one({'name': group, 'votes': update_by})

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


