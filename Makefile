# Variables
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Default task
.DEFAULT_GOAL := help

# Target to create virtual environment
venv:
	python -m venv $(VENV)

# Target to install dependencies
install: venv
	$(PIP) install -r requirements.txt

# Target to run tests
test:
	$(PYTHON) -m pytest

# Target to check code style (e.g., with flake8)
lint:
	$(PYTHON) -m flake8 your_project/

# Target to run tox
tox:
	tox

# Target to clean up virtual environment
clean:
	rm -rf $(VENV)

# Help target to list all available tasks
help:
	@grep '^[a-zA-Z]' Makefile | grep -v ^# | cut -d ':' -f 1 | sort
