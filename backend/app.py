try:
    # 👇️ using Python 3.10+
    from collections.abc import Iterable
except ImportError:
    # 👇️ using Python 3.10-
    from collections import Iterable

import collections.abc

# 👇️ add attributes to `collections` module
# before you import the package that causes the issue
collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

from flask import (
    Flask,
    request,
    jsonify,
    abort
)
import json
from flask_cors import CORS

from database.models import (
    db_drop_and_create_all,
    setup_db,
    setup_migrations,
    Actor,
    Movie,
    Casting
)
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
    setup_migrations(app)

    """
    CORS. Allow '*' for origins.
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})


    '''
    @TODO uncomment the following line to initialize the database
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this function will add data
    '''
    with app.app_context():
        db_drop_and_create_all()


    """
    Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        '''
        CORS Headers
        '''
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response


    """
    Routes
    """


    @app.route("/")
    def index():
        return jsonify(
            {
                "succes": True,
                "message": "Welcome to our Casting Agency"
            }
        )


    @app.route("/actors", methods=["GET"])
    def retrieve_actors():
        actors = Actor.query.order_by(Actor.fullname).all()

        if len(actors) == 0:
            abort(404)
                
        return jsonify({
            "success": True,
            "actors": [actor.format_json() for actor in actors]
        })
    
    @app.route("/movies", methods=["GET"])
    # @requires_auth("get:movies")
    def retrieve_movies():
        movies = Movie.query.order_by(Movie.release_date, Movie.title).all()

        if len(movies) == 0:
            abort(404)
        
        return jsonify({
            "success": True,
            "movies": [movie.format_json() for movie in movies]
        })

    @app.route("/actors/create", methods=["POST"])
    @requires_auth("post:actors")
    def add_actor(payload):
        body = request.get_json()

        if not ("first_name" in body or
                "last_name" in body or
                "age" in body or
                "gender" in body or
                "email" in body or
                "phone" in body or
                "photo_link" in body or
                "seeking_movie" in body):
            abort(422)

        first_name = body.get("first_name", None)
        last_name = body.get("last_name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)
        email = body.get("email", None)
        phone = body.get("phone", None)
        photo_link = body.get("photo_link", None)
        seeking_movie = body.get("seeking_movie", None)

        try:
            actor = Actor(
                first_name=first_name,
                last_name=last_name,
                age=age,
                gender=gender,
                email=email,
                phone=phone,
                photo_link=photo_link,
                seeking_movie=seeking_movie
            )
            actor.insert()
            return jsonify({
                "success": True,
                "added_actor_id": actor.id,
                "added_actor_full_name": actor.fullname,
                "actors": len(Actor.query.order_by(Actor.fullname).all())
            })

        except Exception:
            abort(422)


    @app.route("/movies/create", methods=["POST"])
    @requires_auth("post:movies")
    def add_movie(payload):
        body = request.get_json()

        if not ("title" in body or
                "genres" in body or
                "release_date" in body or
                "seeking_actor" in body):
            abort(422)

        title = body.get("title", None)
        genres = body.get("genres", None)
        release_date = body.get("release_date", None)
        seeking_actor = body.get("seeking_actor", None)

        try:
            movie = Movie(
                title=title,
                genres=genres,
                release_date=release_date,
                seeking_actor=seeking_actor
            )
            movie.insert()
            return jsonify({
                "success": True,
                "added_movie_id": movie.id,
                "added_movie_title": movie.title,
                "movies": len(Movie.query.order_by(Movie.release_date, Movie.title).all())
            })

        except Exception:
            abort(422)

    """
    Error handler for 400, 404, 405, 422, 500
    """


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
            "message": "Resource Not Found"
        }), 404


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405
    

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable resource"
        }), 422


    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500


    """
    Error handler for AuthError
    """


    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error["description"]
        }), error.status_code

    
    return app


# Initializing the app for gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
