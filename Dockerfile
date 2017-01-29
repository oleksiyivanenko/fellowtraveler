FROM python:2.7-alpine

RUN apk add --update \
    nginx \
    supervisor \
    python-dev \
    build-base \
    libffi-dev \
    linux-headers \
    pcre-dev \
    py-pip \
    vim \
    postgresql-dev \
  && rm -rf /var/cache/apk/* && \
  chown -R nginx:www-data /var/lib/nginx

RUN pip install https://github.com/unbit/uwsgi/archive/uwsgi-2.0.zip#egg=uwsgi

ADD . /ft
WORKDIR /ft

RUN pip install -r src/.meta/packages
