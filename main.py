from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Union
import os
from db import create_connection

app = FastAPI()

## create connection to MongoDB
mongoConnString = os.environ['MONGODB_CONNECTION']
mc = create_connection(mongoConnString)
mcd = mc[os.environ['MONGODB_DBNAME']]

class QuestionInfo(BaseModel):
    question: str = Query(default=None, max_length=20000, min_length=10)
    answer: str = Query(default=None, max_length=20000, min_length=10)
    doc_name: str
    id: Union[int, None] = None

@app.post("/send/question/")
async def send_questions(question: QuestionInfo):
    return {"message": question.doc_name}