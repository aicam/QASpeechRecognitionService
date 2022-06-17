import pymongo

from src.req_models import *
import hashlib


# users table
def GetUserDict(user: User):
    return {"username": user.username, "passwprd": user.password, "role": user.role}

def create_connection(connectionString):
    return pymongo.MongoClient(connectionString)


def DB_add_QA_document(mcd, question: QuestionInfo):
    col = mcd[question.doc_name]
    newQA = {'type': question.type, 'question': question.question, 'answer': question.answer}
    return col.insert_one(newQA).inserted_id

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
    hashTxt = hashKey + userDB.username + userDB.password
    return hashlib.md5(hashTxt.encode()).hexdigest()