# Design-Right-Software-web

## Mysql and Mongodb are in docker containers

docker-compose up

## Run backend

python3 manage.py runserver 0.0.0.0:6688

## Install related packages

pip3 install -r requirements

## Update mysql databases

python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate

## Run frontend

npm run serve

