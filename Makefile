.PHONY: build test start

build:
	pipenv install --dev

lint:
	pipenv run flake8 --max-line-length=120 --max-complexity=10 .

test: lint
	pipenv run pytest --cov=application --cov-report xml

start:
	pipenv run python run.py

build-docker:
	docker build .

build-kubernetes:
	docker build -f _infra/docker/Dockerfile .