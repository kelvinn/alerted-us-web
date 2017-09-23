FROM python:2.7.11-slim
ENV PYTHONUNBUFFERED 1
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install --fix-missing -y libffi-dev python-psycopg2 uwsgi python-lxml libpq-dev python-dev binutils libproj-dev gdal-bin libxml2-dev libxslt1-dev && rm -rf /var/lib/apt/lists/*
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
ENV PYTHONPATH $PYTHONPATH:/usr/lib/python2.7/dist-packages
ADD requirements.txt /code/
RUN pip install -r requirements.txt --upgrade
ADD . /code/
CMD ["./run.sh"]