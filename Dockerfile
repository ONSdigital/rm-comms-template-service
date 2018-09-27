FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip3 install pipenv==8.3.1 && pipenv install --deploy --system

EXPOSE 8182

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

COPY . /usr/src/app
