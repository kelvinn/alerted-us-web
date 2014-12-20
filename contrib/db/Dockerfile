FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

# Update the sources list
RUN apt-get update
RUN apt-get install -y libpq-dev python-dev python-lxml python-psycopg2 python-pip binutils libproj-dev gdal-bin libxml2-dev libxslt1-dev
RUN pip install -r requirements.txt
ADD . /code/
