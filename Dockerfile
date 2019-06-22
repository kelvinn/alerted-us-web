FROM alpine:3.9.4
ENV PYTHONUNBUFFERED 1
RUN apk add \
  --no-cache \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
  gdal gdal-dev proj-dev
RUN apk update && apk upgrade
RUN apk add binutils python2-dev libpq postgresql-dev py2-psycopg2 py2-lxml libffi-dev gcc make  \
libxml2-dev libxml2 libxslt py2-pip musl-dev
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
ENV PYTHONPATH $PYTHONPATH:/usr/lib/python2.7/site-packages
ADD requirements.txt /code/
RUN pip install -r requirements.txt --upgrade
ADD . /code/
CMD ["./run.sh"]