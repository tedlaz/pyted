FROM alpine
RUN apk update
RUN apk add python3
RUN apk add py3-psycopg2
RUN apk add py-pillow
RUN pip3 install django
RUN pip3 install dj-database-url
RUN pip3 install django-crispy-forms
RUN pip3 install gunicorn
RUN pip3 install olefile
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
