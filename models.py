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
    CheckConstraint,
    Enum,
)
from sqlalchemy.orm import relationship, column_property, backref
from flask_migrate import Migrate
import enum
from datetime import datetime


# Take environment variables from ".env"
# (file should be in the root directory of your project)
load_dotenv()

DB_PATH = os.getenv("DATABASE_URL")

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # See the SQL queries being printed on the terminal
    # app.config["SQLALCHEMY_ECHO"] = True
    app.debug = True
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


def setup_migrations(app):
    migrate = Migrate(app, db, render_as_batch=False)
    migrate.init_app(app, db, render_as_batch=False)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    movie1 = Movie(
        title="Big house",
        genres=["TV show"],
        release_date="2023.08.01",
        seeking_actor=True,
    )

    movie2 = Movie(
        title="Smile",
        genres=["Comedy"],
        release_date="2023.12.12",
        seeking_actor=True,
    )

    movie3 = Movie(
        title="Cry cry cry",
        genres=["Drama"],
        release_date="2024.12.12",
        seeking_actor=True,
    )

    movie1.insert()
    movie2.insert()
    movie3.insert()

    actor1 = Actor(
        first_name="Sandy",
        last_name="Proom",
        fullname="Sandy Proom",
        age="20",
        gender=GenderType.female,
        email="sandyproom@gnmail.com",
        phone="1234567890",
        photo_link="https://images.unsplash.com/photo-1631084655463-e671365ec05f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
        seeking_movie=True,
    )

    actor2 = Actor(
        first_name="Luna",
        last_name="Grey",
        fullname="Luna Grey",
        age="25",
        gender=GenderType.female,
        email="lunagrey@gnmail.com",
        phone="1234567891",
        photo_link="https://images.unsplash.com/photo-1508326099804-190c33bd8274?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
        seeking_movie=False,
    )

    actor3 = Actor(
        first_name="John",
        last_name="Holms",
        fullname="John Holms",
        age="32",
        gender=GenderType.male,
        email="johnholms@gnmail.com",
        phone="1234567892",
        photo_link="https://images.unsplash.com/photo-1542583701-20d3be307eba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=770&q=80",
        seeking_movie=True,
    )

    actor1.insert()
    actor2.insert()
    actor3.insert()

    casting1 = Casting(
        actor_id=1,
        movie_id=1,
        role="main",
        casting_date="2023.01.10 10:00:00",
        casting_address="123 DHfghjkd street, New York, NY, 12345",
        status=StatusType.in_process,
    )

    casting2 = Casting(
        actor_id=3,
        movie_id=1,
        role="second",
        casting_date="2022.12.01 15:30:00",
        casting_address="123 DHfghjkd street, New York, NY, 12345",
        status=StatusType.accept,
    )

    casting3 = Casting(
        actor_id=3,
        movie_id=2,
        role="second",
        casting_date="2023.10.01 15:00:00",
        casting_address="123 DHfghjkd street, New York, NY, 12345",
        status=StatusType.in_process,
    )

    casting1.insert()
    casting2.insert()
    casting3.insert()


class DbTransactions:
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class GenderType(enum.Enum):
    male = "male"
    female = "female"


class StatusType(enum.Enum):
    accept = "accept"
    reject = "reject"
    in_process = "in process"


class Movie(db.Model, DbTransactions):
    __tablename__ = "Movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genres = Column(ARRAY(String(120)), nullable=False)
    release_date = Column(DateTime, default=datetime.now)
    seeking_actor = Column(Boolean, nullable=False, default=True)
    castings = relationship(
        "Casting", backref=backref("movie", lazy="joined"), cascade="all, delete"
    )

    def __init__(self, title, genres, release_date, seeking_actor):
        self.title = title
        self.genres = genres
        self.release_date = release_date
        self.seeking_actor = seeking_actor

    def format_json(self):
        ordered_keys = [
            "id",
            "title",
            "genres",
            "release_date",
            "seeking_actor",
            "accepted_actors",
            "casting_total",
            "castings_upcoming",
            "castings_past",
            "casting_reject",
        ]

        data = {
            "id": self.id,
            "title": self.title,
            "genres": self.genres,
            "release_date": str(self.release_date),
            "seeking_actor": self.seeking_actor,
            "accepted_actors": [
                {"actor": casting.actor.fullname, "role": casting.role}
                for casting in self.castings
                if casting.status == StatusType.accept
            ],
            "casting_total": len(self.castings),
            "castings_upcoming": len(
                [
                    casting
                    for casting in self.castings
                    if casting.casting_date > datetime.now()
                ]
            ),
            "castings_past": len(
                [
                    casting
                    for casting in self.castings
                    if casting.casting_date <= datetime.now()
                ]
            ),
            "casting_reject": len(
                [
                    casting
                    for casting in self.castings
                    if casting.status == StatusType.reject
                ]
            ),
        }

        ordered_data = {key: data[key] for key in ordered_keys}

        return ordered_data

    def __repr__(self):
        return f"Movie: {self.id}, {self.title} \
                ({self.genres}), \
                need actors: {self.seeking_actor}, \
                release_date: {self.release_date}"


class Actor(db.Model, DbTransactions):
    __tablename__ = "Actors"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    fullname = column_property(first_name + " " + last_name)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(120), unique=True, nullable=False)
    photo_link = Column(String(500), nullable=False)
    seeking_movie = Column(Boolean, nullable=False, default=True)
    castings = relationship(
        "Casting", backref=backref("actor", lazy="joined"), cascade="all, delete"
    )
    __table_args__ = (CheckConstraint(age > 0, name="check_valid_age"), {})

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
        seeking_movie,
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

        ordered_keys = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "age",
            "gender",
            "email",
            "phone",
            "photo_link",
            "seeking_movie",
            "casting_total",
            "castings_upcoming",
            "castings_past",
            "casting_reject",
            "movies_success",
        ]

        data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.fullname,
            "age": self.age,
            "gender": str(self.gender.value),
            "email": self.email,
            "phone": self.phone,
            "photo_link": self.photo_link,
            "seeking_movie": self.seeking_movie,
            "casting_total": len(self.castings),
            "castings_upcoming": len(
                [
                    casting
                    for casting in self.castings
                    if casting.casting_date > datetime.now()
                ]
            ),
            "castings_past": len(
                [
                    casting
                    for casting in self.castings
                    if casting.casting_date <= datetime.now()
                ]
            ),
            "casting_reject": len(
                [
                    casting
                    for casting in self.castings
                    if casting.status == StatusType.reject
                ]
            ),
            "movies_success": [
                {"movie": casting.movie.title, "role": casting.role}
                for casting in self.castings
                if casting.status == StatusType.accept
            ],
        }

        ordered_data = {key: data[key] for key in ordered_keys}

        return ordered_data

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
    actor_id = Column(Integer, ForeignKey("Actors.id", ondelete="cascade"))
    movie_id = Column(Integer, ForeignKey("Movies.id", ondelete="cascade"))
    role = Column(String(120), nullable=False)
    casting_date = Column(DateTime, default=datetime.now)
    casting_address = Column(String(250), nullable=False)
    status = Column(Enum(StatusType), nullable=False)

    def __init__(self, actor_id, movie_id, role, casting_date, casting_address, status):
        self.actor_id = actor_id
        self.movie_id = movie_id
        self.role = role
        self.casting_date = casting_date
        self.casting_address = casting_address
        self.status = status

    def format_json(self):
        return {
            "id": self.id,
            "movie_name": self.movies.title,
            "actor_name": self.actors.fullname,
            "role": self.role,
            "casting_date": str(self.casting_date),
            "casting_address": self.casting_address,
            "status": str(self.status.value),
        }

    def __repr__(self):
        return f"{self.casting_date}: \
                    movie: {self.movies.title}, \
                    actor: {self.actors.first_name} {self.actors.last_name} \
                    ({self.role}). Status: {self.status.value}"
