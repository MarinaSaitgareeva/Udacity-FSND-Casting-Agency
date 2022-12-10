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

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort, redirect
from flask_cors import CORS

from models import (
    setup_db,
    db_drop_and_create_all,
    setup_migrations,
    Actor,
    Movie,
    Casting,
)
from auth.auth import AuthError, requires_auth


load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
CLIENT_ID = os.getenv("CLIENT_ID")
CALLBACK_URI = os.getenv("CALLBACK_URI")


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
    setup_migrations(app)

    """
    CORS. Allow '*' for origins.
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO uncomment the following line to initialize the database
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this function will add data
    """
    with app.app_context():
        db_drop_and_create_all()

    """
    Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        """
        CORS Headers
        """
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    """
    Routes
    """

    @app.route("/")
    def index():
        return jsonify({"success": True, "message": "Welcome to our Casting Agency"})

    @app.route("/login")
    def redirect_login():
        login_url = f"https://{AUTH0_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={CLIENT_ID}&redirect_uri={CALLBACK_URI}"
        return redirect(login_url)

    @app.route("/logout")
    def redirect_logout():
        logout_url = f"https://{AUTH0_DOMAIN}/v2/logout"
        return redirect(logout_url)

    @app.route("/actors", methods=["GET"])
    @requires_auth("get:actors")
    def retrieve_actors(payload):
        actors = Actor.query.order_by(Actor.fullname).all()

        if len(actors) == 0:
            abort(404)

        return jsonify(
            {"success": True, "actors": [actor.format_json() for actor in actors]}
        )

    @app.route("/movies", methods=["GET"])
    @requires_auth("get:movies")
    def retrieve_movies(payload):
        movies = Movie.query.order_by(Movie.release_date, Movie.title).all()

        if len(movies) == 0:
            abort(404)

        return jsonify(
            {"success": True, "movies": [movie.format_json() for movie in movies]}
        )

    @app.route("/actors/<int:actor_id>", methods=["GET"])
    @requires_auth("get:actors")
    def retrieve_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        return jsonify({"success": True, "actor": actor.format_json()})

    @app.route("/movies/<int:movie_id>", methods=["GET"])
    @requires_auth("get:movies")
    def retrieve_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        return jsonify({"success": True, "movie": movie.format_json()})

    @app.route("/actors/create", methods=["POST"])
    @requires_auth("post:actor")
    def add_actor(payload):
        try:
            body = request.get_json()

            if (
                "first_name" not in body
                or "last_name" not in body
                or "fullname" not in body
                or "age" not in body
                or "gender" not in body
                or "email" not in body
                or "phone" not in body
                or "photo_link" not in body
                or "seeking_movie" not in body
            ):
                abort(422)

            first_name = body.get("first_name", None)
            last_name = body.get("last_name", None)
            fullname = body.get("fullname", None)
            age = body.get("age", None)
            gender = body.get("gender", None)
            email = body.get("email", None)
            phone = body.get("phone", None)
            photo_link = body.get("photo_link", None)
            seeking_movie = body.get("seeking_movie", None)

            actor = Actor(
                first_name=first_name,
                last_name=last_name,
                fullname=fullname,
                age=age,
                gender=gender,
                email=email,
                phone=phone,
                photo_link=photo_link,
                seeking_movie=seeking_movie,
            )
            actor.insert()

            return jsonify(
                {
                    "success": True,
                    "added_actor_id": actor.id,
                    "added_actor_full_name": actor.fullname,
                    "actors_total": len(Actor.query.all()),
                }
            )

        except Exception:
            abort(422)

    @app.route("/movies/create", methods=["POST"])
    @requires_auth("post:movie")
    def add_movie(payload):
        body = request.get_json()

        if not (
            "title" in body
            or "genres" in body
            or "release_date" in body
            or "seeking_actor" in body
        ):
            abort(400)

        title = body.get("title", None)
        genres = body.get("genres", None)
        release_date = body.get("release_date", None)
        seeking_actor = body.get("seeking_actor", None)

        try:
            movie = Movie(
                title=title,
                genres=genres,
                release_date=release_date,
                seeking_actor=seeking_actor,
            )
            movie.insert()

            return jsonify(
                {
                    "success": True,
                    "added_movie_id": movie.id,
                    "added_movie_title": movie.title,
                    "movies_total": len(Movie.query.all()),
                }
            )

        except Exception:
            abort(422)

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def modify_actor(payload, actor_id):
        try:
            body = request.get_json()

            if (
                "first_name" not in body
                or "last_name" not in body
                or "fullname" not in body
                or "age" not in body
                or "gender" not in body
                or "email" not in body
                or "phone" not in body
                or "photo_link" not in body
                or "seeking_movie" not in body
            ):
                abort(422)

            first_name = body.get("first_name", None)
            last_name = body.get("last_name", None)
            fullname = body.get("fullname", None)
            age = body.get("age", None)
            gender = body.get("gender", None)
            email = body.get("email", None)
            phone = body.get("phone", None)
            photo_link = body.get("photo_link", None)
            seeking_movie = body.get("seeking_movie", None)

            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.first_name = first_name
            actor.last_name = last_name
            actor.fullname = fullname
            actor.age = age
            actor.gender = gender
            actor.email = email
            actor.phone = phone
            actor.photo_link = photo_link
            actor.seeking_movie = seeking_movie

            actor.update()

            return jsonify({"success": True, "modified_actor": actor.format_json()})

        except Exception:
            abort(404)

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def modify_movie(payload, movie_id):
        try:
            body = request.get_json()

            if (
                "title" not in body
                or "genres" not in body
                or "release_date" not in body
                or "seeking_actor" not in body
            ):
                abort(422)

            title = body.get("title", None)
            genres = body.get("genres", None)
            release_date = body.get("release_date", None)
            seeking_actor = body.get("seeking_actor", None)

            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.title = title
            movie.genres = genres
            movie.release_date = release_date
            movie.seeking_actor = seeking_actor

            movie.update()

            return jsonify({"success": True, "modified_movie": movie.format_json()})

        except Exception:
            abort(404)

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            # if len(actor.castings) > 0:
            #     return (
            #         jsonify(
            #             {
            #                 "success": False,
            #                 "error": 422,
            #                 "message": "Unprocessable resource. There are castings associated with this actor",
            #             }
            #         ),
            #         422,
            #     )

            actor.delete()

            return jsonify({"success": True, "deleted_actor": actor.format_json()})

        except Exception:
            abort(404)

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            # if len(movie.castings) > 0:
            #     return (
            #         jsonify(
            #             {
            #                 "success": False,
            #                 "error": 422,
            #                 "message": "Unprocessable resource. There are castings associated with this movie",
            #             }
            #         ),
            #         422,
            #     )

            movie.delete()

            return jsonify({"success": True, "deleted_movie": movie.format_json()})

        except Exception:
            abort(404)

    """
    Error handler for 400, 404, 405, 422, 500
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Unprocessable resource"}
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal server error"}
            ),
            500,
        )

    """
    Error handler for AuthError
    """

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": error.status_code,
                    "message": error.error["description"],
                }
            ),
            error.status_code,
        )

    return app


# Initializing the app for gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
