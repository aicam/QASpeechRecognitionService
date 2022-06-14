from fastapi import FastAPI
import os
from db import *
from utils import *
from req_models import *

app = FastAPI()

## create connection to MongoDB
mc = create_connection(os.environ['MONGODB_CONNECTION'])
mcd = mc[os.environ['MONGODB_DBNAME']]



@app.post("/send/question/")
async def send_questions(question: QuestionInfo):
    return create_http_message_response(True, add_QA_document(mcd, question))