from fastapi import FastAPI, Request
import os
from src.db import *
from src.score_match import ScoreMatch
from src.utils import *
from src.req_models import *
from starlette.responses import Response

app = FastAPI()

## create connection to MongoDB
mc = create_connection(os.environ['MONGODB_CONNECTION'])
mcd = mc[os.environ['MONGODB_DBNAME']]

## server hash key
hashKey = os.environ['HASH_KEY']

## create new score matching to provide scoring functions
sm = ScoreMatch()

## authorization middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    auth, username = request.headers.get("Authorization"), request.headers.get("Username")
    print(request.url)
    if auth == None or username == None:
        return Response('Authorization failed!!', status_code= 401)
    token = DB_get_user_token_middleware(mcd, hashKey, username)
    # if token == "" or token != auth:
    #     return create_http_message_response(False, "Authorization failed!!")
    response = await call_next(request)
    return response

@app.post("/add/user")
async def add_user(user: User):
    return create_http_message_response(True, str(DB_add_user(mcd, user)))

@app.post("/get/user/token")
async def get_user_token(user: User):
    ok, token = DB_get_user_token(mcd, hashKey, user)

    if not ok:
        return create_http_message_response(False, str("Authentication failed!!"))
    return create_http_message_response(True, token)


@app.post("/send/question/")
async def send_questions(question: QuestionInfo):
    if question.type == 'simple_question':
        sm.store_sentence(question.question + " " + question.answer)
    else:
        sm.store_sentence(question.question)
    return create_http_message_response(True, str(DB_add_QA_document(mcd, question)))
