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

RUN rm /etc/nginx/nginx.conf
RUN ln -s /ft/conf/nginx/nginx.conf /etc/nginx/
RUN ln -s /ft/conf/nginx/ft.conf /etc/nginx/conf.d/

RUN rm /etc/supervisord.conf
RUN ln -s /ft/conf/supervisord/supervisord.conf /etc/

EXPOSE 80 443

CMD ["supervisord", "-n"]
