SHELL := /bin/bash

dev:
		tox && source .tox/dev/bin/activate && python manage.py runserver

collectstatic:
		source .tox/dev/bin/activate && python3 manage.py collectstatic

makemigrations:
		source .tox/dev/bin/activate && python3 manage.py makemigrations

migrate:
		source .tox/dev/bin/activate && python3 manage.py migrate

.PHONY: help

help:
        @grep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'