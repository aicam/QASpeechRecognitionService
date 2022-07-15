import os

from fastapi import FastAPI, Request
from src.db import *
from src.score_match import ScoreMatch
from src.utils import *
from src.req_models import *
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## create connection to MongoDB
mc = create_connection(os.environ['MONGODB_CONNECTION'])
mcd = mc[os.environ['MONGODB_DBNAME']]

## AES encryption class
aes = AESCipher(os.environ['SERVER_KEY'])

## server hash key
hashKey = os.environ['HASH_KEY']

## create new score matching to provide scoring functions
sm = ScoreMatch()

## check admin user is created
DB_initiate_users(mcd)

## authorization middleware
@app.middleware("http")
async def auth_check_midd(request: Request, call_next):
    if request.scope["method"] == "OPTIONS":
        return await call_next(request)
    ## unprotected routes
    if '/get/user/token' in str(request.url):
        response = await call_next(request)
        return response

    auth = request.headers.get("Authorization")
    print(auth)
    if auth == None:
        return Response('Authorization failed!!', status_code= 401)
    try:
        username = aes.decrypt(auth.encode())
    except:
        return Response('Authorization failed!!', status_code=401)
    role = DB_get_user_token_middleware(mcd, aes, username)
    ## check add user done by admin
    if '/add/user' in str(request.url):
        if role != "admin":
            return Response('Authorization failed!!', status_code=401)
    request.headers.__setattr__("username", username)
    response = await call_next(request)
    return response

## user functionalities
@app.post("/add/user")
async def add_user(user: User):
    return create_http_message_response(True, str(DB_add_user(mcd, user)))

@app.post("/get/user/token")
async def get_user_token(user: User):
    ok, token = DB_get_user_token(mcd, user, aes)
    if not ok:
        return create_http_message_response(False, str("Authentication failed!!"))
    return create_http_message_response(True, token)

# core functionalities
@app.post("/send/question/")
async def send_questions(question: QuestionInfo):
    if question.type == 'simple_question':
        sm.store_sentence(question.question + " " + question.answer)
    else:
        sm.store_sentence(question.question)
    return create_http_message_response(True, str(DB_add_QA_document(mcd, question)))


@app.get("/get/data/")
async def get_all_docs(doc_name: Union[str, None] = None):

    return DB_get_all_QA(mcd, doc_name)

@app.post("/answer/")
async def get_answer(askMe: AskMe):
    return DB_answer(mcd, sm, askMe.question, askMe.doc_name)
