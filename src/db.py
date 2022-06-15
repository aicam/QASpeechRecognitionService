import pymongo

from src.req_models import *


def create_connection(connectionString):
    return pymongo.MongoClient(connectionString)


def add_QA_document(mcd, question: QuestionInfo):
    col = mcd[question.doc_name]
    newQA = {'type': question.type, 'question': question.question, 'answer': question.answer}
    return col.insert_one(newQA).inserted_id


