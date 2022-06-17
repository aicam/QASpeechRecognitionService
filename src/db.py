import os

import pymongo

from src.req_models import *
import hashlib

from src.score_match import ScoreMatch


def create_connection(connectionString):
    return pymongo.MongoClient(connectionString)

def GetUserDict(user: User):
    return {"username": user.username, "password": user.password, "role": user.role}


# users table
def DB_initiate_users(mcd):
    userDB = mcd["users"].find_one()
    if userDB == None:
        user = User(username=os.environ["ADMIN_USERNAME"], password=os.environ["ADMIN_PASSWORD"])
        user.role = "admin"
        DB_add_user(mcd, user)

def DB_add_user(mcd, user: User):
    newUser = GetUserDict(user)
    return mcd["users"].insert_one(newUser).inserted_id

def DB_get_user_token(mcd, hashKey: str, user: User):
    userDB = mcd["users"].find_one(GetUserDict(user))
    if userDB == None:
        return False, ""
    hashTxt = hashKey + user.username + user.password
    return True, hashlib.md5(hashTxt.encode()).hexdigest()

def DB_get_user_token_middleware(mcd, hashKey: str, username: str):
    userDB = mcd["users"].find_one({"username": username})
    if userDB == None:
        return ""
    hashTxt = hashKey + userDB['username'] + userDB['password']
    return hashlib.md5(hashTxt.encode()).hexdigest(), userDB['role']

# QA tables
def DB_add_QA_document(mcd, question: QuestionInfo):
    col = mcd[question.doc_name]
    newQA = {'type': question.type, 'question': question.question, 'answer': question.answer}
    return col.insert_one(newQA).inserted_id

def DB_get_all_QA(mcd, doc_name = None):
    qas = {}
    collections = [c for c in mcd.list_collection_names() if c != "users"] if doc_name == None else [doc_name]
    for collection in collections:
        col_qas = []
        for qa in mcd[collection].find():
            newQA = {'question': qa['question'],
                     'type': qa['type'],
                     'answer': qa['answer']}
            col_qas.append(newQA)
        qas.update({collection: col_qas})
    return qas

def DB_answer(mcd, sm: ScoreMatch, question: str, doc_name = None):
    # record top score answers in anses
    anses = []
    top_score = 0
    collections = [c for c in mcd.list_collection_names() if c != "users"] if doc_name == None else [doc_name]
    for collection in collections:
        for qa in mcd[collection].find():
            print(qa.keys())
            newQA = {'question': qa['question'],
                     'type': qa['type'],
                     'answer': qa['answer'],
                     'doc_name': collection}

            score = sm.score_q(question, newQA['question'])
            newQA.update({'score': score})

            # if we have multiple answers with same score, we make an array of them
            if score == top_score:
                anses.append(newQA)

            # if we have found new score better than previous ones, we clear previous answers and replace it with a new array with one element which is the toppest score
            if score > top_score:
                top_score = score
                anses = [newQA]

    return anses