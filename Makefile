.PHONY: run-server
run-server:
	python manage.py runserver

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: migrations
migrations:
	python manage.py makemigrations