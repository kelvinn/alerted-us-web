#!/bin/bash

# Abort the script if any command fails
set -e

# Call this like deploy.sh heroku-app-name https://some-name.com
# Do not include a trailing slash
# heroku-app-name = name of app on Heroku
# https://some-name.com = where to run smoketest

APP_NAME=$1
SMOKE_URL=$2

if ! foobar_loc="$(type -p "heroku")" || [ -z "/usr/local/bin/" ]; then
  brew install heroku/brew/heroku
fi

if [ "$CI" == true ]; then
  docker logout
fi

touch ~/.netrc && chmod 600 ~/.netrc
echo "Printing some Heroku information"
heroku --version
heroku status

echo "Display some Docker information"
docker info

echo "Login to Heroku Container"
heroku container:login --verbose

echo "Show that I'm actually logged in"
heroku apps:info shrouded-citadel-27610

echo "Deleting any earlier built images - not great, I know."
docker images

echo "Push container to Heroku"
heroku container:push web --app $APP_NAME

echo "Release container on Heroku"
heroku container:release web --app $APP_NAME

# Wait for deploy to finish. Not pretty, I know.

sleep 10

# Create a virtual environment
python -m venv .venv && source .venv/bin/activate

git status

python -m pip install requests pyOpenSSL ndg-httpsclient pyasn1
python tests/smoke.py $SMOKE_URL

# Deploy should have succeeded now, so posting release

#export REVISION=`git log -n 1 --pretty="format:%H"`
#export BRANCH=`git rev-parse --abbrev-ref HEAD`
#export URL=https://intake.opbeat.com/api/v1/organizations/$ORGANIZATION_ID/apps/$APP_ID/releases/
#curl $URL -H "Authorization: Bearer $SECRET_TOKEN" -d rev=$REVISION -d branch=$BRANCH -d status=completed