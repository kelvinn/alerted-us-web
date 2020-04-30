FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y binutils python3-dev libpq5 python3-psycopg2 python3-lxml libffi-dev \
build-essential libxml2-dev libxslt1-dev libxml2 libxslt1.1 python3-pip musl-dev gdal-bin libgdal-dev libproj-dev
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
ENV PYTHONPATH $PYTHONPATH:/usr/lib/python3.8/site-packages
ADD requirements.txt /code/
RUN pip install -r requirements.txt --upgrade
ADD . /code/
CMD ["./run.sh"]