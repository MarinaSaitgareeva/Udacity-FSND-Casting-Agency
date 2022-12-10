import os
from dotenv import load_dotenv
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import (
    setup_db,
    db_drop_and_create_all,
    Movie,
    Actor,
    Casting,
)


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_TEST_NAME = os.getenv("DB_TEST_NAME")

CASTING_ASSISTANT_TOKEN = os.getenv("CASTING_ASSISTANT_TOKEN")
CASTING_DIRECTOR_TOKEN = os.getenv("CASTING_DIRECTOR_TOKEN")
EXECUTIVE_PRODUCER_TOKEN = os.getenv("EXECUTIVE_PRODUCER_TOKEN")
INVALID_TOKEN = os.getenv("INVALID_TOKEN")
EXPIRED_TOKEN = os.getenv("EXPIRED_TOKEN")


class CastingAgencyTestCase(unittest.TestCase):
    """
    This class represents the casting agency test case
    """

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_PATH = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_TEST_NAME}"
        )
        setup_db(self.app, self.DB_PATH)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # ---------------------------------------#
    # Test actors endpoints
    # ---------------------------------------#
    def test_retrieve_actors(self):
        res = self.client().get(
            "/actors", headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])
        self.assertGreater(len(data["actors"]), 0)

    def test_401_retrieve_actors_with_no_authorization_headers(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Authorization header is expected")

    def test_401_invalid_token_error(self):
        res = self.client().get(
            "/actors", headers={"Authorization": f"Bearer {INVALID_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unable to parse authentication token.")

    def test_401_expired_token_error(self):
        res = self.client().get(
            "/actors", headers={"Authorization": f"Bearer {EXPIRED_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Token expired.")

    def test_405_use_not_allowed_method(self):
        res = self.client().post(
            "/actors", headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    def test_retrieve_actor(self):
        with self.app.app_context():
            actors = Actor.query.all()
        actor_id = actors[0].id
        res = self.client().get(
            "/actors/" + str(actor_id),
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreater(len(data["actor"]), 0)
        self.assertEqual(data["actor"]["id"], actor_id)

    def test_404_retrieve_actor_which_does_not_exist(self):
        res = self.client().get(
            "/actors/100000",
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_add_actor(self):
        actor = {
            "first_name": "test_actor",
            "last_name": "test_actor",
            "fullname": "test_actor test_actor",
            "age": 18,
            "gender": "male",
            "email": "testuser@gmail.com",
            "phone": "0000000000",
            "photo_link": "https://images.unsplash.com/photo-1631084655463-e671365ec05f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "seeking_movie": True,
        }
        res = self.client().post(
            "/actors/create",
            data=json.dumps(actor),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["added_actor_id"])
        self.assertEqual(data["added_actor_full_name"], "test_actor test_actor")
        self.assertGreater(data["actors_total"], 0)

    def test_422_add_actor_with_not_enough_data(self):
        actor = {
            "first_name": "test_actor",
            "last_name": "test_actor",
            "fullname": "test_actor test_actor",
        }
        res = self.client().post(
            "/actors/create",
            data=json.dumps(actor),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable resource")

    def test_422_add_actor_with_incorrect_data_format(self):
        actor = {
            "first_name": "test_actor",
            "last_name": "test_actor",
            "fullname": "test_actor test_actor",
            "age": "NOT INTEGER!!!",
            "gender": "male",
            "email": "testuser@gmail.com",
            "phone": "0000000000",
            "photo_link": "https://images.unsplash.com/photo-1631084655463-e671365ec05f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "seeking_movie": True,
        }
        res = self.client().post(
            "/actors/create",
            data=json.dumps(actor),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable resource")

    def test_401_add_actor_unauthorized(self):
        actor = {
            "first_name": "test_actor",
            "last_name": "test_actor",
            "fullname": "test_actor test_actor",
            "age": 18,
            "gender": "male",
            "email": "testuser@gmail.com",
            "phone": "0000000000",
            "photo_link": "https://images.unsplash.com/photo-1631084655463-e671365ec05f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "seeking_movie": True,
        }
        res = self.client().post(
            "/actors/create",
            data=json.dumps(actor),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    def test_modify_actor(self):
        with self.app.app_context():
            actor = Actor.query.filter(Actor.id == 1).one_or_none()
        modified_actor = {
            "first_name": "Sandy",
            "last_name": "Proom",
            "fullname": "Sandy Proom",
            "age": 20,
            "gender": "female",
            "email": "sandyproom@gmail.com",
            "phone": "1234567890",
            "photo_link": "https://images.unsplash.com/photo-1631084655463-e671365ec05f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "seeking_movie": True,
        }
        res = self.client().patch(
            "/actors/" + str(actor.id),
            data=json.dumps(modified_actor),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["modified_actor"])
        self.assertEqual(data["modified_actor"]["id"], actor.id)

    def test_404_modify_actor_which_does_not_exist(self):
        modified_actor = {
            "first_name": "Sandy",
            "last_name": "Proom",
            "fullname": "Sandy Proom",
            "age": "20",
            "gender": "female",
            "email": "sandyproom@gmail.com",
            "phone": "1234567890",
            "photo_link": "https://images.unsplash.com/photo-1631084655463-e671365ec05f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "seeking_movie": True,
        }
        res = self.client().patch(
            "/actors/10000",
            data=json.dumps(modified_actor),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_401_modify_actor_unauthorized(self):
        with self.app.app_context():
            actor = Actor.query.filter(Actor.id == 1).one_or_none()
        modified_actor = {
            "first_name": "Sandy",
            "last_name": "Proom",
            "fullname": "Sandy Proom",
            "age": "20",
            "gender": "female",
            "email": "sandyproom@gmail.com",
            "phone": "1234567890",
            "photo_link": "https://images.unsplash.com/photo-1631084655463-e671365ec05f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
            "seeking_movie": True,
        }
        res = self.client().patch(
            "/actors/" + str(actor.id),
            data=json.dumps(modified_actor),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    def test_delete_actor(self):
        res = self.client().delete(
            "/actors/1", headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted_actor"])
        self.assertEqual(data["deleted_actor"]["id"], 1)

    def test_404_delete_actor_which_does_not_exist(self):
        res = self.client().delete(
            "/actors/10000",
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_401_delete_actor_unauthorized(self):
        res = self.client().delete(
            "/actors/1", headers={"Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    # ---------------------------------------#
    # Test movies endpoints
    # ---------------------------------------#
    def test_retrieve_movies(self):
        res = self.client().get(
            "/movies", headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])
        self.assertGreater(len(data["movies"]), 0)

    def test_401_retrieve_movies_with_no_authorization_headers(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Authorization header is expected")

    def test_405_use_not_allowed_method(self):
        res = self.client().post(
            "/movies", headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    def test_retrieve_movie(self):
        with self.app.app_context():
            movies = Movie.query.all()
        movie_id = movies[0].id
        res = self.client().get(
            "/movies/" + str(movie_id),
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreater(len(data["movie"]), 0)
        self.assertEqual(data["movie"]["id"], movie_id)

    def test_404_retrieve_movie_which_does_not_exist(self):
        res = self.client().get(
            "/movies/100000",
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_add_movie(self):
        movie = {
            "title": "test_movie",
            "genres": ["test_movie"],
            "release_date": "2040.01.01",
            "seeking_actor": True,
        }
        res = self.client().post(
            "/movies/create",
            data=json.dumps(movie),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["added_movie_id"])
        self.assertEqual(data["added_movie_title"], "test_movie")
        self.assertGreater(data["movies_total"], 0)

    def test_422_add_movie_with_not_enough_data(self):
        movie = {
            "title": "test_movie",
            "seeking_actor": True,
        }
        res = self.client().post(
            "/movies/create",
            data=json.dumps(movie),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable resource")

    def test_422_add_movie_with_incorrect_data_format(self):
        movie = {
            "title": "test_movie",
            "genres": ["test_movie"],
            "release_date": "2040.01.01",
            "seeking_actor": "NOT BOOLEAN!!!",
        }
        res = self.client().post(
            "/movies/create",
            data=json.dumps(movie),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable resource")

    def test_401_add_movie_unauthorized(self):
        movie = {
            "title": "test_movie",
            "genres": ["test_movie"],
            "release_date": "2040.01.01",
            "seeking_actor": True,
        }
        res = self.client().post(
            "/movies/create",
            data=json.dumps(movie),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    def test_modify_movie(self):
        with self.app.app_context():
            movie = Movie.query.filter(Movie.id == 1).one_or_none()
        modified_movie = {
            "title": "Smiles",
            "genres": ["Comedy"],
            "release_date": "2023.12.12",
            "seeking_actor": True,
        }
        res = self.client().patch(
            "/movies/" + str(movie.id),
            data=json.dumps(modified_movie),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["modified_movie"])
        self.assertEqual(data["modified_movie"]["id"], movie.id)

    def test_404_modify_movie_which_does_not_exist(self):
        modified_movie = {
            "title": "Smiles",
            "genres": ["Comedy"],
            "release_date": "2023.12.12",
            "seeking_actor": True,
        }
        res = self.client().patch(
            "/movies/10000",
            data=json.dumps(modified_movie),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_401_modify_movie_unauthorized(self):
        with self.app.app_context():
            movie = Movie.query.filter(Movie.id == 1).one_or_none()
        modified_movie = {
            "title": "Smiles",
            "genres": ["Comedy"],
            "release_date": "2023.12.12",
            "seeking_actor": True,
        }
        res = self.client().patch(
            "/movies/" + str(movie.id),
            data=json.dumps(modified_movie),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")

    def test_delete_movie(self):
        res = self.client().delete(
            "/movies/1", headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted_movie"])
        self.assertEqual(data["deleted_movie"]["id"], 1)

    def test_404_delete_movie_which_does_not_exist(self):
        res = self.client().delete(
            "/movies/10000",
            headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER_TOKEN}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_401_delete_movie_unauthorized(self):
        res = self.client().delete(
            "/movies/1", headers={"Authorization": f"Bearer {CASTING_ASSISTANT_TOKEN}"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Permission not found.")


if __name__ == "__main__":
    unittest.main()
