# Alerted (Web)

Find out about emergency information that might impact you.

This is the code for the web application side of things written using Python/Django.

# Development

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

You will probably also need to load some geocodes to test geospatial queries.

    $ cd apps/alertdb
    $ python geocode_tools.py

The geocode_tools.py script will download 100MB of data, so don't do it over 3G :)

# What's next?

+ Continue refactoring API and Android app
+ Publish API docs (even basic ones just for auth)
+ Better isolate the apps (microservices)


