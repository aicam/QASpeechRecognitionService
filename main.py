from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Union
import os

app = FastAPI()

mc = os.environ['MONGODB_CONNECTION']


class QuestionInfo(BaseModel):
    question: str = Query(default=None, max_length=20000, min_length=10)
    doc_name: str
    id: Union[int, None] = None

@app.post("/send/question/")
async def send_questions(question: QuestionInfo):
    return {"message": question.doc_name}