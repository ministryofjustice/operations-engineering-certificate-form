.ONESHELL:

# Define the new namespace variable that can be passed as an argument
NAMESPACE_NAME ?= default-namespace

all:
# Run MegaLinter
lint:
	npx mega-linter-runner -e 'SHOW_ELAPSED_TIME=true'

flake8: venv
	venv/bin/pip3 install flake8
	venv/bin/flake8 --config=./.flake8 --exclude=venv,__pycache__,.pytest_cache,.venv .

trivy-scan:
	@echo "Running Trivy scan..."
	docker build -t localbuild/testimage:latest .
	trivy image --severity HIGH,CRITICAL localbuild/testimage:latest

# Build the Docker image
build:
	docker-compose build

# Run the Docker container
up:
	docker-compose up -d

# Stop and remove the Docker container
down:
	docker-compose down

# View logs for the running container
logs:
	docker-compose logs -f app

# Open a shell inside the running app container
shell:
	docker exec -it operations-engineering-flask-application /bin/sh

# Target to run the Python script with pipenv, passing the namespace name
# make new-namespace NAMESPACE_NAME=my-new-namespace
new-namespace:
	pipenv run python -m bin.make_new_cloud_platform_namespace $(NAMESPACE_NAME)

# Target to clean the pipenv environment
clean:
	pipenv --rm

local:
	pipenv install --dev
	pipenv run python -m app.run

.PHONY: build up down logs shell trivy-scan lint all
