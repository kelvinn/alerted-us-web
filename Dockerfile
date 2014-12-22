# Set the base image to Python
FROM python:2.7

# Update the sources list
RUN apt-get update
RUN apt-get upgrade -y

# Install Python and Basic Python Tools
RUN apt-get install -y libpq-dev python-dev python-lxml python-psycopg2 python-pip binutils libproj-dev gdal-bin libxml2-dev libxslt1-dev

# Install web server components
RUN apt-get install -y nginx supervisor

# Install uwsgi
RUN pip install uwsgi

ADD requirements.txt /app/requirements.txt

# Get pip to download and install requirements:
RUN pip install -r /app/requirements.txt

# Copy the application folder inside the container
ADD . /app

# Setup config files
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /app/contrib/web/django.conf /etc/nginx/sites-enabled/
RUN ln -s /app/contrib/web/supervisor.conf /etc/supervisor/conf.d/

# Expose ports
EXPOSE 80 8000 8080

# Set the default directory where CMD will execute
WORKDIR /app

CMD ["/bin/sh", "-e", "run.sh"]
