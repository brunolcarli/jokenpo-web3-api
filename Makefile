install:
	pip3 install -r requirements.txt

run:
	python3 manage.py runserver 0.0.0.0:8898

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
