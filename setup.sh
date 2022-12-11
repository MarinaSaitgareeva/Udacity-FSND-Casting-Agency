#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/casting_agency"
export DATABASE_TEST_URI="postgresql://postgres:5432/casting_agency_test"

export FLASK_APP=app.py
export FLASK_DEBUG=True

export AUTH0_DOMAIN="fs2022nd.us.auth0.com"
export API_AUDIENCE="Casting_Agency_FSND"
export ALGORITHMS=["RS256"]

export CLIENT_ID="HtJZ7kKWkhIqL3l306Lq0G2JHlaTnZqY"
export CALLBACK_URI="http://127.0.0.1:8080"
# export CALLBACK_URI="https://udacity-fsnd-casting-agency-ms.herokuapp.com/"

export EXCITED="true"


echo "setup.sh script executed successfully!"