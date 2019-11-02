# Alerted (Web)

Find out about emergency information that might impact you.

This is the code for the web application side of things written using Python/Django.

# Development

[![Build Status](https://travis-ci.org/kelvinn/alerted-us-web.svg?branch=master)](https://travis-ci.org/kelvinn/alerted-us-web)

[![Coverage Status](https://coveralls.io/repos/github/kelvinn/alerted-us-web/badge.svg?branch=master)](https://coveralls.io/github/kelvinn/alerted-us-web?branch=master)

The fastest way to get going is to use Docker Compose.

Download Docker and Docker Compose; install them. Then...

    $ cd alerted-us-web
    $ docker-compose start db
    $ docker-compose start redis

This will install all known dependencies and configure a database for you. Next, you can set the superuser account and start Django's development server within Docker:

    $ docker-compose run web python manage.py createsuperuser
    $ docker-compose run web python manage.py migrate
    $ docker-compose run -p web python manage.py runserver 0.0.0.0:8000

Browse to http://127.0.0.1:8000 and you should see the index page, or http://127.0.0.1:8000/admin for the admin UI.

Tests can be run like so:

    $ docker-compose run web python manage.py test

The virtual framebuffer might not start automatically (is usually does). If this is the case, simple start it:

    $ sudo /etc/init.d/xvfb start

Xvfb is needed for a limited number of Selenium tests.

You will probably also need to load some geocodes to test geospatial queries.

    $ docker-compose run web python apps/alertdb/geocode_tools.py

The geocode_tools.py script will download 100MB of data, so don't do it over 3G :)

# What's next?

+ Fix performance issues when Postgres gets large
+ Publish API docs (even basic ones just for auth)
