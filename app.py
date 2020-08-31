import os
from flask_cors import CORS
import json
from flask import Flask, render_template, request, Response, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref
from models import setup_db, db, Movie, Director
from auth.auth import AuthError, requires_auth
from sqlalchemy.exc import SQLAlchemyError


def create_app(test_config=None):
    # variable set to 'prod' when production and set to 'dev' while
    ENV = 'dev'
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)
    migrate = Migrate(app, db)

    @app.after_request
    def after_request(response):
        response.headers.add
        ('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add
        ('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
        return response

    # the default endpoint ,will render html file instead of the front end
    @app.route('/')
    def index():
        return render_template('index.html')

    # endpoint to get the all movies,needs the auth of user and admin
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):

        try:
            # get all the movie from DB
            movies = Movie.query.all()

            if len(movies) == 0:
                Movies_list = {}
            else:
                Movies_list = []

                for movie in movies:

                    Movies_list.append({
                        "id": movie.id,
                        "title": movie.title,
                        "rate": movie.rate,
                        "directors": 
                        [director.id for director in Director.query.filter_by(
                            movie_id=movie.id).all()]

                    })

            return jsonify({
                'Movies_list': Movies_list,
                'status': 200,
                'success': True,
            })
        except Exception:
            abort(422)
    # endpoint to get directors list ,needs the auth of user and admin

    @app.route('/directors', methods=['GET'])
    @requires_auth('get:directors')
    def get_directors(payload):

        try:
            # get all the directors from DB
            directores = Director.query.all()
            if len(directores) == 0:
                directores_list = {}
            else:
                directores_list = []
                for director in directores:
                    directores_list.append({
                        "id": director.id,
                        "name": director.name,
                        "movie_id": director.movie_id
                    })
            return jsonify({
                'directores_list': directores_list,
                'status': 200,
                'success': True,
            })
        except Exception:
            abort(422)

    # this endpoint to add a movie to the DB , only admin can add

    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(payload):
        body = request.get_json()

        if 'movie_title' not in body:
            abort(422)
        if 'movie_rate' not in body:
            abort(422)
        try:
            movie_title = body['movie_title']
            movie_rate = body['movie_rate']
            movie = Movie(title=movie_title, rate=movie_rate)
            movie.insert()
            return jsonify({
                'id' : movie.id,
                'status': 200,
                'success': True,
            })
        except Exception:
            abort(422)
    # this endpoint to add a director to the DB , only admin can add

    @app.route('/director', methods=['POST'])
    @requires_auth('post:director')
    def add_director(payload):
        body = request.get_json()
        director_name = body.get('director_name', None)
        movie_id = body.get('movie_id', None)
        if director_name is None or movie_id is None:
            abort(422)
        try:
            director = Director(name=director_name, movie_id=movie_id)
            director.insert()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except Exception:
            abort(422)

    # this endpoint to update a movie information , only admin can

    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(422)

        body = request.get_json()

        try:
            if 'movie_title' in body:
                movie.title = body.get('movie_title')
            if 'movie_rate' in body:
                movie.rate = body.get('movie_rate')
            movie.update()
            return jsonify({
                'status': 200,
                'success': True
            })
        except Exception:
            abort(422)

    # this endpoint to delete a movie frome the DB , only admin can
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).first()

        if movie is None:
            abort(404)

        try:
            directors = Director.query.filter_by(movie_id=movie.id).all()
            if len(directors) != 0:
                for director in directors:
                    director.delete()
            movie.delete()
            return jsonify({
                'status': 200,
                'success': True,
            })
        except Exception:
            abort(422)

    '''
    Error Handling
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exciption):
        response = jsonify(exciption.error)
        response.status_code = exciption.status_code
        return response

    print(__name__, flush=True)
    if __name__ == '__main__':
        # check if we are the in production or developing mood
        if ENV == 'dev':
            app.run(host='127.0.0.1', port=5000, debug=True)
        else:
            app.run(debug=False)

    return app
