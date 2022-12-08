import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
    ARRAY,
    CheckConstraint)
from sqlalchemy.orm import relationship, column_property
from flask_migrate import Migrate
from enum import Enum
import datetime


# Take environment variables from ".env"
# (file should be in the root directory of your project)
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1:5432")
DB_NAME = os.getenv("DB_NAME", casting_agency)
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_PATH = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # See the SQL queries being printed on the terminal
    app.config["SQLALCHEMY_ECHO"] = True
    app.debug = True
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


def setup_migrations(app):
    migrate = Migrate(app, db, render_as_batch=False)


# TODO change drink -> actor + movie
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    movie1 = Movie(
        title="Movie 1",
        genres="[Genre1, Genre2]",
    
    )

    movie1.insert()


class DbTransactions:
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Movie(db.Model, DbTransactions):
    """
    Movies
    Have title and release date
    """
    __tablename__ = "Movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genres = Column(ARRAY(String), nullable=False)
    release_date = Column(DateTime, default=datetime.datetime.now)
    casting = relationship(
                        "Casting",
                        backref="movies",
                        lazy="joined",
                        cascade="all, delete")

    def __init__(self, title, genres, release_date):
        self.title = title
        self.genres = genres,
        self.release_date = release_date

    def format_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "genres": self.genres,
            "release_date": self.release_date,
            "actors": [actor for actor in self.casting.actors.fullname]
        }

    def __repr__(self):
        return f'Movie: {self.id}, {self.title}'


class Actor(db.Model, DbTransactions):
    """
    Actors
    Have full name, age and gender
    """
    __tablename__ = "Actors"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    fullname = column_property(first_name + " " + last_name)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("Male", "Female", name="gender"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(120), unique=True, nullable=False)
    photo_link = Column(String(500), nullable=False)
    seeking_movie = Column(Boolean, nullable=False, default=False)
    casting = relationship(
        "Casting",
        backref="actors",
        lazy="joined",
        cascade="all, delete")
    __table_args__ = CheckConstraint(age > 0, name="check_valid_age")

    def __init__(
        self,
        first_name,
        last_name,
        fullname,
        age,
        gender,
        email,
        phone,
        photo_link,
        seeking_movie
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.fullname = fullname
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone
        self.photo_link = photo_link
        self.seeking_movie = seeking_movie

    def format_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.fullname,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "movies": [movie for movie in self.casting.movies.title]
        }

    def __repr__(self):
        return f"Actor: {self.id}, \
                    {self.first_name} {self.first_name} \
                    ({self.age}, {self.gender})"


"""
Association_table: Casting - many-to-many relationship between Actor and Movie
"""


class Casting(db.Model, DbTransactions):
    __tablename__ = "Casting"

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("artists.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    role = Column(String(120), nullable=False)
    casting_date = Column(DateTime, default=datetime.datetime.now)
    status = Column(
        Enum("Accept", "Reject", name="status"),
        nullable=False)

    def __init__(self, actor_id, movie_id, role, casting_date, status):
        self.actor_id = actor_id
        self.movie_id = movie_id
        self.role = role
        self.casting_date = casting_date
        self.status = status

    def format_json(self):
        return {
            "id": self.id,
            "movie_name": self.movies.title,
            "actor_name": self.actors.fullname,
            "role": self.role,
            "casting_date": self.casting_date,
            "status": self.status
        }

    def __repr__(self):
        return f"{self.casting_date}: \
                    movie: {self.movies.title}, \
                    actor: {self.actors.first_name} {self.actors.last_name} \
                    ({self.role}). Status: {self.status}"
