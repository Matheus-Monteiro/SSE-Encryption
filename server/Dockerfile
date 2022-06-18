FROM python:3-alpine
RUN apk add --virtual .build-dependencies \
    --no-cache \
    python3-dev \
    build-base \
    linux-headers \
    pcre-dev 
RUN apk add --no-cache pcre
WORKDIR /server
COPY . /server
# RUN apk update && apk add g++ gcc libxml2 libxslt-dev
RUN python -m pip install --upgrade pip
RUN pip install -r /server/requirements.txt
RUN pip install uwsgi
RUN apk del .build-dependencies && rm -rf /var/cache/apk/*
EXPOSE 5003
CMD ["uwsgi", "--ini", "/server/wsgi.ini"]