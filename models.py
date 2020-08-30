import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import backref
import psycopg2


ENV = 'prod'

if ENV == 'dev':
    database_name = "capstone"
    database_path = "postgres://{}/{}".format('postgres:aisha_abdullah@localhost:5432', database_name)
else:
    database_name = "capstone"
    database_path = os.environ['DATABASE_URL']
    conn = psycopg2.connect(database_path, sslmode='require')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movie
'''


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    rate = Column(Integer,nullable=False)
    director = db.relationship('Director', backref='movie', lazy=True)

    def __init__(self, title,rate):
        self.title = title
        self.rate=rate
        
        


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'rate': self.rate,
            'director':self.director
        }



'''
director
'''


class Director(db.Model):
    __tablename__ = 'director'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    
    def __init__(self, name,movie_id):
        self.name = name
        self.movie_id = movie_id
        

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }


