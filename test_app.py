import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only

from app import create_app
from models import setup_db, Movie, Actor
from config import assistant_token, director_token, producer_token



class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'superadmin', 'localhost:5432',
                                                             self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            "title": "Avengers: End game",
            "release_date": "04-22-2019"
        }

        self.new_actor = {
            "name": "Robert Downey Jr",
            "age": 55,
            "gender": "male"
        }

        
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """ Executed after each test"""
        pass

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers=assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_method_not_allowed_on_all_movies(self):
        res = self.client().put('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_update_specific_movie(self):
        movie = Movie.query.first()
        movie_id = movie.id

        res = self.client().patch('/movies/{}'.format(movie_id), json={'title': 'Hitman'}, headers=director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_delete_specific_movie(self):
        movie = Movie.query.first()
        movie_id = movie.id

        res = self.client().delete('/movies/{}'.format(movie_id), headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)

    def test_method_not_allowed_on_specific_movie(self):
        movie = Movie.query.first()
        movie_id = movie.id

        res = self.client().post('/movies/{}'.format(movie_id), json={'title': 'Hitman'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
    
    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_all_actors(self):
        res = self.client().get('/actors', headers=assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_method_not_allowed_on_all_actors(self):
        res = self.client().delete('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_update_specific_actor(self):
        actor = Actor.query.first()
        actor_id = actor.id

        res = self.client().patch('/actors/{}'.format(actor_id), json={'name': 'Peter Parkers', 'age': 32}, headers=director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_specific_actor(self):
        actor = Actor.query.first()
        actor_id = actor.id

        res = self.client().delete('/actors/{}'.format(actor_id), headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)

    def test_method_not_allowed_on_specific_actor(self):
        actor = Actor.query.first()
        actor_id = actor.id

        res = self.client().put('/actors/{}'.format(actor_id), json={'name': 'Vin Diesel', 'age': 46, 'gender': 'male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()