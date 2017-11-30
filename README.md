# RM Comms Template
[![Build Status](https://travis-ci.org/ONSdigital/rm-comms-template-service.svg?branch=master)](https://travis-ci.org/ONSdigital/rm-comms-template-service) 

## Overview
This is the RAS Comms Template micro-service.


## Setup
Install postgresql
```bash
brew install postgresql
```

Install pipenv
```bash
pip install pipenv
```

Use pipenv to create a virtualenv and install dependencies
```bash
pipenv install
```
## Running
[Install Docker](https://docs.docker.com/engine/installation/)
```bash
docker-compose up
```
To test the service is up:

```
curl http://localhost:8081/info
```

## Database

The database will automatically be created when starting the application.