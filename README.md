# Search Engine Service to Store Q/A and searching
This project is developed to store different questions and answers in 
a MongoDB and can return an answer based on question similarity with questions stored in the database.

## Users
When server is started, if it couldn't find any user in the database.
It will automatically create an admin user with environment variables.
Endpoints are developed as:
```http request
POST /add/user
{
    "username": "<admin username>",
    "password": "<admin password>"
}
"add new user to database (requires admin role)"

POST /get/user/token
{
    "username": "<username>",
    "password": "<password>",
    "role": "<role (optional)> default = customer"
}
"return user token to be used on Authorization header (no auth check)"
```
Each user should add token and username to `Authorization` and `Username` headers respectively.

## Q/A
Each question has two types of answers which are saved in same format. Each question
model has a question, answer, type and a doc_name which is equal to the collection name in mongodb database.
When a new question is sent, it is stored in the document mentioned and when
a new question is asked, web service will search over all collections or a specific one which is mentioned int the request.
```http request
POST /send/question/
{
    "question": "<question string>",
    "answer": "<answer string>",
    "doc_name": "<document name string>",
    "type": "<type of question (optional)> default = simple_question"
}
"add new question and answer to database"

GET /get/data/<doc_name (optional)>
"return all questions and answers."
"if doc_name is mentioned, only questions in the specified collection are returned."

POST /answer/
{
    "question": "<question string>"
    "doc_name": "<document name (optional)>"
}
"return all questions with highest score in all collections or in
collection (doc_name) specified."
```

## Scoring Function
All scoring functions and calculations are written in `src/score_match.py`.
It is based on tf-idf scoring. Every time a new question is sent to the server,
it saves all new word counts in question and answer (if the type of question
is `simple_question`). When a new question is asked, it will calculate the score of
matching of the question to all documents or the document specified in the request.
Matching function is based on sum of scores of all vocabs in both questions, divided
by the length of question asked from the server.
Count of all words are stored in vocabs.json.
<br>
**Calculation of question and database questions score**

$$ score = \sum_i^{common-vocabs}{vocab-score(vocabs[i])} $$

**Calculation of vocab score (vocab-score)**
if not in vocab dictionary, score = 1 otherwise: <br>
$$ vocab-score = 1 / count-of-vocab $$
