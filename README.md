# Design-Right-Software-web

## Mysql and Mongodb are in docker containers

docker-compose up

## Run backend

python3 manage.py runserver 0.0.0.0:6688

## Update mysql databases

python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate

## Run frontend

npm run serve
