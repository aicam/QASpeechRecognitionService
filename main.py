from fastapi import FastAPI
import os
from src.db import *
from src.score_match import ScoreMatch
from src.utils import *
from src.req_models import *

app = FastAPI()

## create connection to MongoDB
mc = create_connection(os.environ['MONGODB_CONNECTION'])
mcd = mc[os.environ['MONGODB_DBNAME']]

## create new score matching to provide scoring functions
sm = ScoreMatch()

@app.post("/send/question/")
async def send_questions(question: QuestionInfo):
    if question.type == 'simple_question':
        sm.store_sentence(question.question + " " + question.answer)
    else:
        sm.store_sentence(question.question)
    return create_http_message_response(True, str(add_QA_document(mcd, question)))
