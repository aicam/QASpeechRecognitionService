from pydantic import BaseModel
from typing import Union
from fastapi import Query

class QuestionInfo(BaseModel):
    question: str = Query(default=None, max_length=20000, min_length=10)
    answer: str = Query(default=None, max_length=20000, min_length=10)
    doc_name: str
    id: Union[int, None] = None