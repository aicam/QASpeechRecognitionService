# Search Engine Service to Store Q/A and searching
This project is developed to store different questions and answers in 
a MongoDB and can return an answer based on question similarity with questions stored in the database.

## Users
When server is started, if it couldn't find any user in the database.
It will automatically create an admin user with environment variables.
Endpoints are developed as:
```http request
POST /add/user
add new user to database (requires admin role)
```