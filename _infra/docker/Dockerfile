# Dockerfile specifically for kubernetes
FROM python:3.8-slim

RUN apt update && apt install -y build-essential curl gunicorn
RUN pip install pipenv

WORKDIR /app

COPY . /app
RUN pipenv install --deploy --system

CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "4", "app:app"]