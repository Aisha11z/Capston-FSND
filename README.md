# Aisha's Capston-FSND
The capstone project intended for the Full-Stack Developer Nanodegree program from Udacity.the project models a system for a Company that is responsible for creating movies and managing and assigning directors to those movies.

frontend comming soon....

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.


- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 
 ##### Running the server

From within the  directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
## Roles and Permissions:
- USER
    - Can view directors and movies list
        - 'get:movies'
        - 'get:directorss'    
 
- ADMIN
    - All permissions a USER has and…
    - Add or delete an movie , add directors from the database
        - 'post:movie'
        - 'delete: movie'
        - 'post:director'
    - Modify movies
        - 'patch:movie'

 Note: Inssed ```setup.sh``` file we have a token for each role, you can copy and Decoded at [jwt](https://jwt.io/) to see permission for each token. 

## Deployment
The API is deployed on Heroku [project link](https://capstone-fsns-2020.herokuapp.com/).

# Endpoints
- GET '/movies'
- GET '/directors'
- POST '/movie'
- POST '/director'
- PATCH '/movie/<int:movie_id>'
- DELETE '/movies/<int:movie_id>'


GET '/movies'
- Fetches a dictionary of movies 
- Request Arguments: None
- Authentication: the roles that can acess are ADMIN and USER
- Returns: A JSON with list of movies objects, status and success value.

```bash
curl --location --request GET 'https://capstone-fsns-2020.herokuapp.com/movies' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVOZjBGQXQ2YlVzMHhkWm01YnJYRCJ9.eyJpc3MiOiJodHRwczovL2NzZnMyMDIwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjRhYzY2ODIwNzZhNzAwNjc4ZWUxZWEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODg4MTUzNCwiZXhwIjoxNTk4ODg4NzM0LCJhenAiOiJ1UHBCYXdkVnNZZXpkSjA1bDJNMW8yM1B6OVllNHZEZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRpcmVjdG9ycyIsImdldDptb3ZpZXMiXX0.UFFVazmntfOPfiTGgP-GmJRtvPlgKO3qTeEVYC5DeqCRFu57dXkv4Ta6uOhd6_CXro2Yh3BFg_uoI0Vw0hQvusmLiMu1D2x1fhcZ26UfE-UpfwLW5q1v7Ur1cLfz3VmTOMujrMeQqZFttHhqTthblb7P-e_LipeAak-KXdiRyHSsmZXBndSn8PxIMRbjkkg44qUlIbVeo9Zqc8EUhs8D6Qec7sdreKgPMwxzBHRMd6dPIRFGlYkDz5GyFSQnJz63xKD38QqwCIWzeAK_HG4BZ59v_m1ksQ0KQzeINEtHBIsOjBGGcVnWhHe9PqYOPfoV6rE043kJ0FUGGrEj3BQrgQ'
```
```bash
{
    "Movies_list":[
        {"directors":[1],
        "id":1,
        "rate":9,
        "title":"X-Man"
        }
    ],
    "status":200,
    "success":true
    }

```
GET '/directors'
- Fetches a dictionary of directors
- Request Arguments: None
- Authentication: the roles that can acess are ADMIN and USER
- Returns: A JSON with list of directors objects,status and success value.
```bash
curl --location --request GET 'https://capstone-fsns-2020.herokuapp.com/directors' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVOZjBGQXQ2YlVzMHhkWm01YnJYRCJ9.eyJpc3MiOiJodHRwczovL2NzZnMyMDIwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjRhYzY2ODIwNzZhNzAwNjc4ZWUxZWEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODg4MTUzNCwiZXhwIjoxNTk4ODg4NzM0LCJhenAiOiJ1UHBCYXdkVnNZZXpkSjA1bDJNMW8yM1B6OVllNHZEZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRpcmVjdG9ycyIsImdldDptb3ZpZXMiXX0.UFFVazmntfOPfiTGgP-GmJRtvPlgKO3qTeEVYC5DeqCRFu57dXkv4Ta6uOhd6_CXro2Yh3BFg_uoI0Vw0hQvusmLiMu1D2x1fhcZ26UfE-UpfwLW5q1v7Ur1cLfz3VmTOMujrMeQqZFttHhqTthblb7P-e_LipeAak-KXdiRyHSsmZXBndSn8PxIMRbjkkg44qUlIbVeo9Zqc8EUhs8D6Qec7sdreKgPMwxzBHRMd6dPIRFGlYkDz5GyFSQnJz63xKD38QqwCIWzeAK_HG4BZ59v_m1ksQ0KQzeINEtHBIsOjBGGcVnWhHe9PqYOPfoV6rE043kJ0FUGGrEj3BQrgQ'
```
```bash
{
    "directores_list":{},
    "status":200,
    "success":true
}
```

POST '/movie'
- Post a movie and persist it to the database
- Request Arguments: A JSON with title, rate  ```eg:{ "movie_title":"titanic", "movie_rate": 9}```
- Authentication: Only the ADMIN
- Returns : A JSON with success value and the status
```bash
curl --location --request POST 'https://capstone-fsns-2020.herokuapp.com/movie' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVOZjBGQXQ2YlVzMHhkWm01YnJYRCJ9.eyJpc3MiOiJodHRwczovL2NzZnMyMDIwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjRhYzY5ODliNzI1NDAwNmQ5YjEyZDgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODg4MTc2MiwiZXhwIjoxNTk4ODg4OTYyLCJhenAiOiJ1UHBCYXdkVnNZZXpkSjA1bDJNMW8yM1B6OVllNHZEZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1vdmllIiwiZ2V0OmRpcmVjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDptb3ZpZSIsInBvc3Q6ZGlyZWN0b3IiLCJwb3N0Om1vdmllIl19.b9CIaj5IdmqRmNpndvI8_XR1tDyUemCZxOknIf-WOdZsGXoHzO_PyKB5GO-WlGFZJcDmZz6XyjYHkvHoZtPMlMycpMHpqfeVsQWIPTSllv2E542V1rGhN77NywBJ0JaObLniKKlmkkS6zRvDV1CdNYRb0rjGcyJDeUqtZ5WqRWMv8ErD-bChgp4uozpwycaSTvLmi8jAnCqwQKpipsbFJfM6aryT1J6ZfKHA0b4mV3utnZjSoJvQHgk40I-jvhHzVI4Oj4cRMAThe8qP3fUINRl-BrxX4uTy26Y9Txx7tICtD0tCVlNslgQyy_zITG8Nx-ZJMBz7ciOuaANrIKAOyg' \
--header 'Content-Type: application/json' \
--data-raw '{ "movie_title":"X-Man", "movie_rate": 9}'
```
```bash
{
    "status":200,
    "success":true
}
```
POST '/director'
- Post director and persist it to the database
- Request Arguments: A JSON with name,The movie that will be his director ```eg:{"director_name":"Lazaro Neto",
"movie_id":1}```
- Authentication: only the ADMIN
- Returns : A JSON with success value and the status
```bash
curl --location --request POST 'https://capstone-fsns-2020.herokuapp.com/director' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVOZjBGQXQ2YlVzMHhkWm01YnJYRCJ9.eyJpc3MiOiJodHRwczovL2NzZnMyMDIwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjRhYzY5ODliNzI1NDAwNmQ5YjEyZDgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODg4MTc2MiwiZXhwIjoxNTk4ODg4OTYyLCJhenAiOiJ1UHBCYXdkVnNZZXpkSjA1bDJNMW8yM1B6OVllNHZEZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1vdmllIiwiZ2V0OmRpcmVjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDptb3ZpZSIsInBvc3Q6ZGlyZWN0b3IiLCJwb3N0Om1vdmllIl19.b9CIaj5IdmqRmNpndvI8_XR1tDyUemCZxOknIf-WOdZsGXoHzO_PyKB5GO-WlGFZJcDmZz6XyjYHkvHoZtPMlMycpMHpqfeVsQWIPTSllv2E542V1rGhN77NywBJ0JaObLniKKlmkkS6zRvDV1CdNYRb0rjGcyJDeUqtZ5WqRWMv8ErD-bChgp4uozpwycaSTvLmi8jAnCqwQKpipsbFJfM6aryT1J6ZfKHA0b4mV3utnZjSoJvQHgk40I-jvhHzVI4Oj4cRMAThe8qP3fUINRl-BrxX4uTy26Y9Txx7tICtD0tCVlNslgQyy_zITG8Nx-ZJMBz7ciOuaANrIKAOyg' \
--header 'Content-Type: application/json' \
--data-raw '{"director_name":"Lazaro Neto","movie_id":1}'
```
```bash
{
   "status":200,
   "success":true
}
```
PATCH '/movie/<int:movie_id>'
- Updates a movie title or rate based on the id 
- Request Arguments: A JSON with title and a rate ```eg: { "movie_title":"The Movie", "movie_rate": 7}```
- Authentication: only the ADMIN
- Returns : A JSON with success value and the status
```bash
curl --location --request PATCH 'https://capstone-fsns-2020.herokuapp.com/movie/1' \
--header 'Authorization: Bearer eeyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVOZjBGQXQ2YlVzMHhkWm01YnJYRCJ9.eyJpc3MiOiJodHRwczovL2NzZnMyMDIwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjRhYzY5ODliNzI1NDAwNmQ5YjEyZDgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODg4MTc2MiwiZXhwIjoxNTk4ODg4OTYyLCJhenAiOiJ1UHBCYXdkVnNZZXpkSjA1bDJNMW8yM1B6OVllNHZEZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1vdmllIiwiZ2V0OmRpcmVjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDptb3ZpZSIsInBvc3Q6ZGlyZWN0b3IiLCJwb3N0Om1vdmllIl19.b9CIaj5IdmqRmNpndvI8_XR1tDyUemCZxOknIf-WOdZsGXoHzO_PyKB5GO-WlGFZJcDmZz6XyjYHkvHoZtPMlMycpMHpqfeVsQWIPTSllv2E542V1rGhN77NywBJ0JaObLniKKlmkkS6zRvDV1CdNYRb0rjGcyJDeUqtZ5WqRWMv8ErD-bChgp4uozpwycaSTvLmi8jAnCqwQKpipsbFJfM6aryT1J6ZfKHA0b4mV3utnZjSoJvQHgk40I-jvhHzVI4Oj4cRMAThe8qP3fUINRl-BrxX4uTy26Y9Txx7tICtD0tCVlNslgQyy_zITG8Nx-ZJMBz7ciOuaANrIKAOyg' \
--header 'Content-Type: application/json' \
--data-raw '{"movie_title":"The Movie", "movie_rate": 7}'
```
```bash
{
   "status":200,
   "success":true
}
```
DELETE '/movies/<int:movie_id>'
- Remove persistentle a movie from the database based on id 
- Request Arguments: id of the movie eg:'/movies/1'
- Returns: A JSON with success value and the status
```bash
curl --location --request DELETE 'https://capstone-fsns-2020.herokuapp.com/movies/1' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVOZjBGQXQ2YlVzMHhkWm01YnJYRCJ9.eyJpc3MiOiJodHRwczovL2NzZnMyMDIwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjRhYzY5ODliNzI1NDAwNmQ5YjEyZDgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODg4MTc2MiwiZXhwIjoxNTk4ODg4OTYyLCJhenAiOiJ1UHBCYXdkVnNZZXpkSjA1bDJNMW8yM1B6OVllNHZEZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1vdmllIiwiZ2V0OmRpcmVjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDptb3ZpZSIsInBvc3Q6ZGlyZWN0b3IiLCJwb3N0Om1vdmllIl19.b9CIaj5IdmqRmNpndvI8_XR1tDyUemCZxOknIf-WOdZsGXoHzO_PyKB5GO-WlGFZJcDmZz6XyjYHkvHoZtPMlMycpMHpqfeVsQWIPTSllv2E542V1rGhN77NywBJ0JaObLniKKlmkkS6zRvDV1CdNYRb0rjGcyJDeUqtZ5WqRWMv8ErD-bChgp4uozpwycaSTvLmi8jAnCqwQKpipsbFJfM6aryT1J6ZfKHA0b4mV3utnZjSoJvQHgk40I-jvhHzVI4Oj4cRMAThe8qP3fUINRl-BrxX4uTy26Y9Txx7tICtD0tCVlNslgQyy_zITG8Nx-ZJMBz7ciOuaANrIKAOyg' \
--data-raw ''
```
```bash
{
   "status":200,
   "success":true
}
```
## API Testing
To create the database for test, run
```bash
dropdb castone_test && createdb castone_test
```
Note: the above command runs on postgres, if have not installed yet [link](https://www.postgresql.org/download/)

To run the tests, run
```bash
python test_app.py
``` 
## Error Handler
They have this format
```bash
{
    'success': False,
    'error': 404,
    'message': 'Resource not found'
}
```
```
    - 400 'bad request'
    - 401 'method not allowed'
    - 404 'Resource not found'
    - 422 'unprocessable'
    - 500 'internal server error'
```
## TO TEST THE APP
1- open the url https://capstone-fsns-2020.herokuapp.com
2- you can use this temperoray acounts I created in auth0 to login:
#####  USER
- USER: abcd@ gmail.com
#####  ADMIN
- ADMIN: abc@ gmail.com
##### password 
- you can use this password for both :Password123
4- after that you can copy the access token from the url and test it in postman or curl as shown above




