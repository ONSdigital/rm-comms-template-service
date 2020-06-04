FROM python:3.8-slim

WORKDIR /app
COPY . /app
EXPOSE 8182
RUN apt-get update -y && apt-get install -y python-pip && apt-get install -y curl
RUN pip3 install pipenv==8.3.1 && pipenv install --deploy --system

ENTRYPOINT ["python3"]
CMD ["run.py"]
