# Udacity-FSND-Casting-Agency

## Motivation for the project

This is the capstone project for Udacity's Fullstack Nanodegree program. It models a casting agency database to facilitate casting and managing actors for the movie industry.

Authorized users (Executive Producer, Casting Director, and Casting Assistant) can interact with the API to view, add, update, and delete movies and actor details contingent on the permissions allowed to each role.

In this Capstone project, I was challenged to use all of the concepts and the skills taught in the courses to build an API from start to finish and host it:

- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

---

## API URL

- \*\*Heroku base URL: https://udacity-fsnd-casting-agency-ms.herokuapp.com
- \*\*Localhost base URL: is http://127.0.0.1:8080

---

## Getting Started

### Installation and Database Setup

Clone the repo by running

```bash
git clone https://github.com/MarinaSaitgareeva/Udacity-FSND-Casting-Agency
```

#### Installing Dependencies

- [Python 3.11.0](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).
- [Flask](http://flask.pocoo.org/) handles requests and responses.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) handles cross origin requests from the frontend server.
- [Flask-Migrate](https://flask-cors.readthedocs.io/en/latest/) is used to handle SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface.
- [PostgreSQL](https://www.postgresql.org/docs/) is the object-relational SQL database system used.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle PostgreSQL database.
- [Unittest](https://docs.python.org/3/library/unittest.html) is the Python testing framework used for unit testing.
- [Auth0](https://auth0.com/docs/api/management/v2) is an adaptable authentication and authorization platform used to implement RBAC.

#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
. venv/bin/activate
```

#### Installing Python Dependencies

Once the virtual environment is setup and running, install the required dependencies by navigating to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.

---

## Database Setup

The project uses **PostgreSQL** databases.

- Create two databases: One for **testing** and one for **development**

```bash
createdb <database_name>
```

- Generate database tables from the saved casting_agency.psql file or the migration files included by executing:

```bash
psql casting_agency < casting_agency.psql
```

or

```bash
python manage.py db upgrade
```

- Set the `DATABASE_URL`, `DATABASE_URL_TEST` (and other variables `AUTH0_DOMAIN`, `API_AUDIENCE`, `ALGORITHMS`, `CLIENT_ID`, `CALLBACK_URI`, `CASTING_ASSISTANT_TOKEN`, `CASTING_DIRECTOR_TOKEN`, `EXECUTIVE_PRODUCER_TOKEN`, `INVALID_TOKEN`, `EXPIRED_TOKEN`), in `.env` file to match the names of your development and testing databases.

## Running the Server

Switch to the project directory and ensure that the virtual environment is running.

### To run the **development** server, execute

```bash
source setup.sh
python3 app.py
```

---

## Testing

Replace the JWT tokens in `.env` with ones generated on the website. JWT tokens expire 24 hours from generation.

For testing locally, stop the development server and reset the database.
The following resets the database and runs the test suite:

```bash
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency_test.psql
python3 test_app.py
```

One Postman collection is also included for further testing.

- `Udacity-FSND-Casting-Agency.postman_collection.json`

To use them install [Postman](https://www.postman.com/downloads/) locally and import the 2 collections. In order for them to work properly, update the Bearer Tokens in each collection with tokens generated from the website. See the Authorization section.

---

## Deployment

This project is deployed to [Heroku](https://heroku.com). To Deploy your own version:

- You must have Git installed and your project must be tracked in a repository
- Install Heroku locally: <https://devcenter.heroku.com/articles/heroku-cli>
- Create your heroku app:

```bash
heroku create <name_of_app> --buildpack heroku/python
```

- Add `heroku` as a Git remote and push your project to `Heroku` (Change `main` to the name of the appropriate git brach if it differs, i.e. `master`)

```bash
git remote add heroku <heroku_git_url>
git push heroku main
```

- Create a postgres database in Heroku:

```bash
heroku addons:create heroku-postgresql:mini --app <name_of_app>
```

- After the database has been created, you would want to set up the Environment variables in the Heroku Cloud, specific to your application. Run the following command to fix your DATABASE_URL configuration variable in Heroku.

```bash
heroku config --app <name_of_app>
```

Copy the DATABASE_URL generated from the step above, and update your local DATABASE_URL environment variable files.

You may set the environment variables in the Heroku portal after you "create" your application. To save the environment variables in the Heroku, you can go to the Heroku dashboard >> Particular App >> Settings >> Reveal Config Vars section and save the variables and their values.

- Go to settings on the [Heroku dashboard](https://dashboard.heroku.com/) for the app you've built and click on `Heroku dashboard >> Particular App >> Settings >> Reveal Config Vars`. You will need to set environmental variables for each variable: `API_AUDIENCE`, `AUTH0_DOMAIN`, `ALGORITHMS`, `CLIENT_ID`, `CALLBACK_URI`, `CASTING_ASSISTANT_TOKEN`, `CASTING_DIRECTOR_TOKEN`, `EXECUTIVE_PRODUCER_TOKEN`.

- Once your app is deployed, run migrations by running:

```bash
heroku run python manage.py db upgrade --app <name_of_app>
```

- To see the Heroku logs for debugging:

```bash
heroku logs --tail
```

- To reset the Heroku database:

```bash
heroku run python manage.py db downgrade --app <name_of_app>
heroku run python manage.py db upgrade --app <name_of_app>
heroku run python manage.py seed --app <name_of_app>
```

Your online app is now ready to go.

---

## API

In order to use the API, users need to be authenticated. JWT tokens can be generated by logging in with the provided credentials on the hosted site.

### Endpoints

- Note: any `curl` commands used must include an authorization header as all endpoints require authorization to use:  
  `curl -H "Authorization: Bearer <JWT_ACCESS_TOKEN>"`
- For post and patch you need you need also add Content-Type:
  `curl -H "Authorization: Bearer <JWT_ACCESS_TOKEN>" -H "Content-Type: application/json" -d "{data}"`

#### GET /login

Redirect the user to login page.

#### GET /logout

Logout from the user account.

#### GET /actors

- Fetches an array of dictionaries for each actor from the database.
- Request Arguments: None.
- Returns:
  - `success` - the success flag.
  - `actors` - an array of dictionaries for each actor from the database.

```json
{
  "actors": [
    {
      "age": 32,
      "casting_reject": 0,
      "casting_total": 2,
      "castings_past": 1,
      "castings_upcoming": 1,
      "email": "johnholms@gnmail.com",
      "first_name": "John",
      "full_name": "John Holms",
      "gender": "male",
      "id": 3,
      "last_name": "Holms",
      "movies_success": [
        {
          "movie": "Big house",
          "role": "second"
        }
      ],
      "phone": "1234567892",
      "photo_link": "https://images.unsplash.com/photo-1542583701-20d3be307eba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=770&q=80",
      "seeking_movie": true
    }
  ],
  "success": true
}
```

#### GET /movies

- Fetches an array of dictionaries for each movie from the database.
- Request Arguments: None.
- Returns:
  - `success` - the success flag.
  - `movies` - an array of dictionaries for each movie from the database.

```json
{
  "movies": [
    {
      "accepted_actors": [
        {
          "actor": "John Holms",
          "role": "second"
        }
      ],
      "casting_reject": 0,
      "casting_total": 2,
      "castings_past": 1,
      "castings_upcoming": 1,
      "genres": ["TV show"],
      "id": 1,
      "release_date": "2023-08-01 00:00:00",
      "seeking_actor": true,
      "title": "Big house"
    }
  ],
  "success": true
}
```

`GET '/actors/int:actor_id'`

- Fetches the specific actor.
- Request Arguments: actor_id (integer) - the actor id.
- Returns:
  - `success` - the success flag.
  - `actor` - the actor detailed data.

```json
{
  "actor": {
    "age": 20,
    "casting_reject": 0,
    "casting_total": 1,
    "castings_past": 0,
    "castings_upcoming": 1,
    "email": "sandyproom@gnmail.com",
    "first_name": "Sandy",
    "full_name": "Sandy Proom",
    "gender": "female",
    "id": 1,
    "last_name": "Proom",
    "movies_success": [],
    "phone": "1234567890",
    "photo_link": "https://images.unsplash.com/photo-1631084655463-e671365ec05f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
    "seeking_movie": true
  },
  "success": true
}
```

`GET '/movies/int:movie_id'`

- Fetches the specific movie.
- Request Arguments: movie_id (integer) - the movie id.
- Returns:
  - `success` - the success flag.
  - `movie` - the movie detailed data.

```json
{
  "movie": {
    "accepted_actors": [
      {
        "actor": "John Holms",
        "role": "second"
      }
    ],
    "casting_reject": 0,
    "casting_total": 2,
    "castings_past": 1,
    "castings_upcoming": 1,
    "genres": ["TV show"],
    "id": 1,
    "release_date": "2023-08-01 00:00:00",
    "seeking_actor": true,
    "title": "Big house"
  },
  "success": true
}
```

`POST '/actors/create'`

- Create a new actor.
- Request Arguments:

  - first_name (string),
  - last_name (string),
  - fullname (string),
  - age (int),
  - gender (string),
  - email (string),
  - phone (string),
  - photo_link (string),
  - seeking_movie (Boolean)

- Returns:
  - `success` - the success flag.
  - `added_actor_id` - the new actor ID.
  - `added_actor_full_name` - the new actor fullname.
  - `actors_total` - number of total actors.

```json
{
  "actors_total": 4,
  "added_actor_full_name": "Kyle 2 Locman 2",
  "added_actor_id": 4,
  "success": true
}
```

`POST '/movies/create'`

- Create a new movie.
- Request Arguments:

  - title (string),
  - genres (array(string)),
  - release_date (date),
  - seeking_actor (Boolean)

- Returns:
  - `success` - the success flag.
  - `added_movie_id` - the new movie ID.
  - `added_movie_title` - the new movie title.
  - `actors_total` - number of total movies.

```json
{
  "actors_total": 4,
  "added_actor_full_name": "Kyle 2 Locman 2",
  "added_actor_id": 4,
  "success": true
}
```

`PATCH '/actors/int:actor_id'`

- Modify the specific actor.
- Request Arguments:
  - actor_id (integer) - the actor id.
  - first_name (string),
  - last_name (string),
  - fullname (string),
  - age (int),
  - gender (string),
  - email (string),
  - phone (string),
  - photo_link (string),
  - seeking_movie (Boolean)
- Returns:
  - `success` - the success flag.
  - `modified_actor` - the modified actor with detailed data.

```json
{
  "modified_actor": {
    "age": 25,
    "casting_reject": 0,
    "casting_total": 0,
    "castings_past": 0,
    "castings_upcoming": 0,
    "email": "lunagrey@gmail.com",
    "first_name": "Luna",
    "full_name": "Luna Grey",
    "gender": "female",
    "id": 2,
    "last_name": "Grey",
    "movies_success": [],
    "phone": "1234567891",
    "photo_link": "https://images.unsplash.com/photo-1508326099804-190c33bd8274?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
    "seeking_movie": false
  },
  "success": true
}
```

`PATCH '/movies/int:movie_id'`

- Modify the specific movie.
- Request Arguments:
  - movie_id (integer) - the movie id.
  - title (string),
  - genres (array(string)),
  - release_date (date),
  - seeking_actor (Boolean)
- Returns:
  - `success` - the success flag.
  - `modified_movie` - the modified movie with detailed data.

```json
{
  "modified_movie": {
    "accepted_actors": [
      {
        "actor": "John Holms",
        "role": "second"
      }
    ],
    "casting_reject": 0,
    "casting_total": 2,
    "castings_past": 1,
    "castings_upcoming": 1,
    "genres": ["Comedy"],
    "id": 1,
    "release_date": "2023-12-12 00:00:00",
    "seeking_actor": true,
    "title": "Smiles"
  },
  "success": true
}
```

`DELETE '/actors/int:actor_id'`

- Delete the actor using the actor ID.
- Request Arguments: actor_id (integer) - the actor id.
- Returns:
  - `success` - the success flag.
  - `deleted_actor` - the deleted actor with detailed data.

```json
{
  "deleted_actor": {
    "age": 25,
    "casting_reject": 0,
    "casting_total": 0,
    "castings_past": 0,
    "castings_upcoming": 0,
    "email": "lunagrey@gmail.com",
    "first_name": "Luna",
    "full_name": "Luna Grey",
    "gender": "female",
    "id": 2,
    "last_name": "Grey",
    "movies_success": [],
    "phone": "1234567891",
    "photo_link": "https://images.unsplash.com/photo-1508326099804-190c33bd8274?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80",
    "seeking_movie": false
  },
  "success": true
}
```

`DELETE '/movies/int:movie_id'`

- Delete the movie using the movie ID.
- Request Arguments: movie_id (integer) - the movie id.
- Returns:
  - `success` - the success flag.
  - `deleted_movie` - the deleted movie with detailed data.

```json
{
  "deleted_movie": {
    "accepted_actors": [
      {
        "actor": "John Holms",
        "role": "second"
      }
    ],
    "casting_reject": 0,
    "casting_total": 2,
    "castings_past": 1,
    "castings_upcoming": 1,
    "genres": ["Comedy"],
    "id": 1,
    "release_date": "2023-12-12 00:00:00",
    "seeking_actor": true,
    "title": "Smiles"
  },
  "success": true
}
```

### Errors

`Error 400`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 400,
  "message": "Bad Request"
}
```

`Error 404`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```

`Error 405`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 405,
  "message": "Method Not Allowed"
}
```

`Error 422`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 422,
  "message": "Unprocessable resource"
}
```

`Error 500`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 500,
  "message": "Internal server error"
}
```

#### AuthErrors

`Error 400`

- Returns: an object with these keys: success, error and message.

```json
{
  "success": false,
  "error": 400,
  "message": "Unable to parse authentication token."
}
```

`Error 401`

- Returns: an object with these keys: success, error and message.
- Permission not found. OR Authorization header is expected. OR Token expired.

```json
{
  "success": false,
  "error": 401,
  "message": "Permission not found."
}
```

### Author

Marina Saitgareeva is the author of this project and all documentation.
