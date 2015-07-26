FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y python-psycopg2 libpq-dev python-dev binutils libproj-dev gdal-bin libxml2-dev libxslt1-dev 
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
CMD ["./run.sh"]