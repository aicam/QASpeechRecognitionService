import pymongo

from req_models import *


def create_connection(connectionString):
    return pymongo.MongoClient(connectionString)


def add_QA_document(mcd, question: QuestionInfo):
    col = mcd[question.doc_name]
    newQA = {'question': question.question, 'answer': question.answer}
    return col.inset_one(newQA).inserted_id


