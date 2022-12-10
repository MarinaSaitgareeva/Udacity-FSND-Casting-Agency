#!/bin/bash
export DATABASE_URL="postgresql://marinas:2001@localhost:5432/casting_agency"
export DATABASE_TEST_URI="postgresql://marinas:2001:5432/casting_agency_test"

export FLASK_APP=app.py
export FLASK_DEBUG=True

export AUTH0_DOMAIN="fs2022nd.us.auth0.com"
export API_AUDIENCE="Casting_Agency_FSND"
export ALGORITHMS=["RS256"]

export CLIENT_ID="HtJZ7kKWkhIqL3l306Lq0G2JHlaTnZqY"
export CLIENT_SECRET="wYCRfDg4e6NbsjjTEARnGWJVk4A4kmoXtg045O9D6bZrPzmbeyZO5sptJEPJBgns"
export CALLBACK_URI="http://127.0.0.1:8080"


echo "setup.sh script executed successfully!"