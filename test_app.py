from app import create_app
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from models import setup_db, db, Movie, Director
from auth.auth import AuthError, requires_auth
from unittest.mock import patch

# Note : if the token expired pleas login using the acounts in readme file 
# and copy them here

bearer_tokens = {
    "movies_admin": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVOZjBGQXQ2YlVzMHhkWm01YnJYRCJ9.eyJpc3MiOiJodHRwczovL2NzZnMyMDIwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjRhYzY5ODliNzI1NDAwNmQ5YjEyZDgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODk3NzU3NCwiZXhwIjoxNTk4OTg0Nzc0LCJhenAiOiJ1UHBCYXdkVnNZZXpkSjA1bDJNMW8yM1B6OVllNHZEZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm1vdmllIiwiZ2V0OmRpcmVjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDptb3ZpZSIsInBvc3Q6ZGlyZWN0b3IiLCJwb3N0Om1vdmllIl19.G3h7q2zY1ikiRq_Rncj09b1l_PBMIxg627_o_eTJ5E3yLCXhQlO5a4Ie7YDA6zq_HuykzMXdKh1iXnk9AkLEWANvnd71ihbvfGpy4Xe2t10Mjg99z_qYz9mBryOSlFyIuGdqC2OkLHJnHTKP57KZ91rIQGkGToS2UHGoX7DQpckh2xKil-i0TXQ_AOQhZhO7jVEKfUT78qDELjIoEHyGI_9p70n-MjMVxCNXMDez5uCNbHV0zmepVBElAefZvVlTwbUSe5whfVi3-jAk-1Wjr34UbS5xSgen0HWl65xLiCBuowZZEBWyX7avMlphiJp1GJ_M3IX_tVfSm_KaH7QrMQ",
    "movies_user": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVOZjBGQXQ2YlVzMHhkWm01YnJYRCJ9.eyJpc3MiOiJodHRwczovL2NzZnMyMDIwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjRhYzY2ODIwNzZhNzAwNjc4ZWUxZWEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU5ODk3NzQ0NSwiZXhwIjoxNTk4OTg0NjQ1LCJhenAiOiJ1UHBCYXdkVnNZZXpkSjA1bDJNMW8yM1B6OVllNHZEZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRpcmVjdG9ycyIsImdldDptb3ZpZXMiXX0.bx1tAGpZojs1CnKl6bbVoVst65Z9rZFXkw6tnq_LySzI_4M_bh0GkFLiKaV_MuYNSgueK7tM7uBF3d04uWpNPZOx2FFIqwzedwooO_kNj5IPdz9MzMk0kgdPIPOmBq7zWWmSelCb5DpODHOl-5mixWCOT6qArpNpivLUtrTiw3SzOyPBIhkxGr-mx_BKAdVGC5ASEqIzVnqiMB4aRZ2JRN15w-yfiBztfiQK-1vWJaFMWuoUuIUSVXaEzmsGieYhnJDArflgfzON6GRpCmg99AZbBtpIqYwzH1sMeK2lxc87EuhB8IqxaciE-I-Uq5S0rITW8a0Ak0_dzS7sPgt10g",

}
movies_admin_auth_header = {
    'Authorization': bearer_tokens['movies_admin']
}

movies_user_auth_header = {
    'Authorization': bearer_tokens['movies_user']
}
'''
Below "mock_decorator" is to mimic a fake JWT token to
bybass the @requires_auth decorator in order to test the
endpoints without having to go through the
authentication process.
'''

class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://{}:{}@{}/{}".format(
        'postgres', 'aisha_abdullah', 'localhost:5432',
         self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    """
    Test each endpoint.
    """
    def test_get_movie_role_based(self):
        res = self.client().get('/movies' , headers=movies_user_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_directors(self):
        res = self.client().get('/directors' , headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_add_movie_success(self):
        #test the success case of adding a movie 
        # with attributes: movie_title,movie_rate
        res = self.client().post('/movie', 
        json = {'movie_title' : 'test_movie', 'movie_rate' : 9 } , headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_add_movie_failure(self):
        # test the failure case of adding 
        # a movie without the attributes
        # which should return a 422 error
        res = self.client().post('/movie',
        json={'movie_title' : None, 'movie_rate' : None}, headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_add_movie_failure_role_based(self):
        # test the failure case of adding by a user 
        # a movie without the attributes
        # which should return a 422 error
        res = self.client().post('/movie',
        json={'movie_title' : 'add movie by admin', 'movie_rate' : 9 },
        headers=movies_user_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['code'], "forbidden")
        self.assertEqual(res.status_code, 401)

    def test_add_director_success(self):
        # test the success case of adding 
        # a director with attributes:
        # director_name,movie_id
        res = self.client().post('/director',
        json={'director_name' : 'aisha', 'movie_id' : 1} , headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_add_director_failure(self):
        # test the failure case of adding a 
        # director without the attributes
        # which should return a 422 error
        res = self.client().post('/director' , json={} , headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_patch_movie_success(self):
        # Successfuly updating the "movie_rate" of the
        # movie with "id": 1 from 9 to 10
        res = self.client().patch('/movie/1',
        json={'movie_rate': 10} , headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
    
    def test_patch_movie_failure(self):
        # test the failure case of updating 
        # a movie without the attributes
        # which should return a 422 error
        res = self.client().patch('/movie/1',
        json={'movie_rate' : None, 'movie_title' : None} , headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_delete_movie_sucess(self):
        # test the success case of  deleting a movie  
        test_movie=Movie(title = 'test', rate = 5)
        test_movie.insert()
        res = self.client().delete('/movies/{}'.format(test_movie.id) , headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_failure(self):
        # test the failure case of deleting 
        # a movie that not exist
        # which should return a 404 error
        res = self.client().delete('/movies/5' , headers=movies_admin_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
        self.assertEqual(data['error'], 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
