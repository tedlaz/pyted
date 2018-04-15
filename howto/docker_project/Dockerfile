FROM alpine
RUN apk update && apk add python3 && apk add py3-psycopg2 && apk add py-pillow && pip3 install django && pip3 install dj-database-url && pip3 install django-crispy-forms && pip3 install gunicorn && pip3 install olefile && mkdir /code 
ENV PYTHONUNBUFFERED 1 
WORKDIR /code
ADD . /code/
