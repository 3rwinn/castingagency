import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response
 
  # Get movies
  @app.route('/movies')
  @requires_auth('view:movies')
  def retrieve_movies(payload):
      movies = Movie.query.order_by(Movie.id).all()
      formatted_movies = [movie.format() for movie in movies]

      if len(movies) == 0:
          abort(404)

      return jsonify({
          'success': True,
          'movies': formatted_movies
      })

  # Create new movie
  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movie')
  def create_movie(payload):
      body = request.get_json()

      new_title = body.get('title', None)
      new_release_date = body.get('release_date', None)

      try:
          movie = Movie(title=new_title, release_date=new_release_date)
          movie.insert()

          return jsonify({
              'success': True,
              'movie': [movie.format()]
          })

      except:
          abort(422)
  
  # Update movie
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('edit:movie')
  def partial_update_movie(payload, movie_id):
      body = request.get_json()

      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

          if movie is None:
              abort(404)
          
          if 'title' in body:
              movie.title = body.get('title')
          
          if 'release_date' in body:
              movie.release_date = body.get('release_date')
          
          movie.update()
          
          return jsonify({
              "success": True,
              "movie": [movie.format()]
          })
      
      except:
          abort(400)
  
  # Delete movie
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(payload, movie_id):
      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

          if movie is None:
              abort(404)
          
          movie.delete()

          return jsonify({
              "success": True,
              "deleted": movie_id
          })

      except:
          abort(422)

  # Get actors
  @app.route('/actors')
  @requires_auth('view:actors')
  def retrieve_actors(payload):
      actors = Actor.query.order_by(Actor.id).all()
      formatted_actors = [actor.format() for actor in actors]

      if len(actors) == 0:
          abort(404)

      return jsonify({
          'success': True,
          'actors': formatted_actors
      })

  # Create new actor
  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actor')
  def create_actor(payload):
      body = request.get_json()

      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender = body.get('gender', None)

      try:
          actor = Actor(name=new_name, age=new_age, gender=new_gender)
          actor.insert()

          return jsonify({
              'success': True,
              'actor': [actor.format()]
          })

      except:
          abort(422)

  # Update actor
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('edit:actor')
  def partial_update_actor(payload, actor_id):
      body = request.get_json()

      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

          if actor is None:
              abort(404)
          
          if 'name' in body:
              actor.name = body.get('name')
          
          if 'age' in body:
              actor.age = body.get('age')
          
          if 'gender' in body:
              actor.gender = body.get('gender')
          
          actor.update()
          
          return jsonify({
              "success": True,
              "actor": [actor.format()]
          })
      
      except:
          abort(400)
  
  # Delete actor
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):
      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

          if actor is None:
              abort(404)
          
          actor.delete()

          return jsonify({
              "success": True,
              "deleted": actor_id
          })

      except:
          abort(422)
  
  # Handle errors  
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "ressource not found"
          }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
          }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400
  
  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"
          }), 405
  
  @app.errorhandler(AuthError)
  def authorization_failed(AuthError):
      return jsonify({
          "success": False,
          "error": AuthError.status_code,
          "message": AuthError.error['description']
          }), AuthError.status_code
  
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)