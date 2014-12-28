# Alerted (Web)

Find out about emergency information that might impact you.

This is the code for the web application side of things written using Python/Django.

# Development

[![Build Status](https://snap-ci.com/nnEwcVUmv5bLOCY7LCABqQnAO-r01AAfNm7lO1lPMTc/build_image)](https://snap-ci.com/kelvinn/alerted-us-web/branch/master)

[![Code Health](https://landscape.io/github/kelvinn/alerted-us-web/master/landscape.png)](https://landscape.io/github/kelvinn/alerted-us-web/master)

The fastest way to get going is to use Vagrant.

Download Vagrant and VirtualBox; install them. Then...

    $ cd alerted-us-web
    $ vagrant up

This will install all known dependencies and configure a database for you. Next, you can
log into the alerted-us-web VM and start Django's development server:

    $ ssh -oPort=2222 vagrant@localhost  # Default pw is 'vagrant'
    $ source /opt/python/venv/bin/activate
    $ cd /vagrant
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver 0.0.0.0:8000

Browse to http://127.0.0.1:8000 and you should see the index page, or http://127.0.0.1:8000/admin for the admin UI.

Tests can be run like so:

    $ python manage.py test

The virtual framebuffer might not start automatically (is usually does). If this is the case, simple start it:

    $ sudo /etc/init.d/xvfb start

Xvfb is needed for a limited number of Selenium tests.

You will probably also need to load some geocodes to test geospatial queries.

    $ cd apps/alertdb
    $ python geocode_tools.py

The geocode_tools.py script will download 100MB of data, so don't do it over 3G :)

# Development (next...)

I'm slowly contemplating Docker, so here are some notes. Start three containers:

#### Postgresql
docker run -e USER=app_user -e PASSWORD=djangouserspassword -e SCHEMA=cozysiren -e POSTGIS=true -p 5432:5432 --rm --name db jamesbrink/postgresql

#### Redis
docker run --rm -p 6379:6379 --name redis redis

#### Alerted web (non-interactive)

docker run --rm -p 80:80 --link redis:redis --link db:db -e RACK_ENV=development -v ~/Workspace/alerted-us-web/:/app kn_test

#### Or Alerted web (interactive)

docker run --rm -p 8080:8080 --link redis:redis --link db:db -e RACK_ENV=development -v ~/Workspace/alerted-us-web/:/app -it --entrypoint=/bin/bash kn_test

# What's next?

+ Continue refactoring API and Android app
+ Publish API docs (even basic ones just for auth)
+ Better isolate the apps (microservices)
