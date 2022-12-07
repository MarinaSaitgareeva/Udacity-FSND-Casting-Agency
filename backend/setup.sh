#!/bin/bash
export DATABASE_URL="postgresql://marinas:2001@localhost:5432/casting_agency"
export DATABASE_TEST_URI="postgresql://marinas:2001:5432/casting_agency_test"

export FLASK_APP=app.py
export FLASK_ENV=development

export AUTH0_DOMAIN=""
export API_AUDIENCE=""
export ALGORITHMS=['RS256']
export SECRET=""


echo "setup.sh script executed successfully!"