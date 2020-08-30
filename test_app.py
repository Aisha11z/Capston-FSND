from app import create_app
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from models import setup_db, db, Movie, Director
from auth.auth import AuthError, requires_auth
from unittest.mock import patch

'''
Below "mock_decorator" is to mimic a fake JWT token to
bybass the @requires_auth decorator in order to test the
endpoints without having to go through the
authentication process.
'''


def mock_decorator(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = 'fake'
            try:
                payload = 'fake'
            except:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description':
                    'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            # check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


patch('app.requires_auth', mock_decorator).start()


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://{}:{}@{}/{}".format(
        'postgres', 'aisha_abdullah','localhost:5432', self.database_name)
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

    def test_add_movie_success(self):
        '''
        test the success case of adding a movie with attributes:
        movie_title,movie_rate
        '''
        res = self.client().post('/movie',json={'movie_title': 'test_movie','movie_rate':9})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_add_movie_failure(self):
        '''
        test the failure case of adding a movie without the attributes
        which should return a 422 error
        '''
        res = self.client().post('/movie',json={'movie_title': None,'movie_rate':None})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)

    def test_add_director_success(self):
        '''
        test the success case of adding a director with attributes:
        director_name,movie_id
        '''
        res = self.client().post('/director',
                                 json={'director_name': 'aisha',
                                 'movie_id':1})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_add_director_failure(self):
        '''
        test the failure case of adding a director without the attributes
        which should return a 422 error
        '''
        res = self.client().post('/director',
                                 json={})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)
    

    def test_patch_movie_success(self):
        '''
        Successfuly updating the "movie_rate" of the
        movie with "id": 1 from
        9 to 10
        '''
        res = self.client().patch('/movie/1',
                                  json={'movie_rate': 10})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        

    def test_patch_movie_failure(self):
        '''
        test the failure case of updating a movie without the attributes
        which should return a 422 error
        '''
        res = self.client().patch('/movie/1',json={'movie_rate': None,'movie_title':None})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")
        self.assertEqual(data['error'], 422)


    def test_delete_movie_sucess(self):
        '''
        test the success case of  deleting a movie  
        '''
        test_movie=Movie(title='test',rate=5)
        test_movie.insert()
        res = self.client().delete('/movies/{}'.format(test_movie.id))
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_failure(self):
        '''
        test the failure case of deleting a movie that not exist
        which should return a 404 error
        ''' 
        res = self.client().delete('/movies/5')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()