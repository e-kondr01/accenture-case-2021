# Django docker project template
Перед началом работы поменять "accenture_case" везде на имя проекта.

## Local deploy
./local.sh

## Production deploy
Добавить в Github HOST, USERNAME и PASSWORD для CI/CD

SSL:

https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71

Прописать следующие команды:

`sudo chown -R 777:777 ./logs/gunicorn`

`sudo chown -R 777:777 ./accenture_case/media`

Т. к. это mounted папки, в которые хотят писать приложения внутри докера. Но они работают не от root, а от пользователя 777:777.

## ТЕСТИРОВАНИЕ

docker exec django bash -c "python manage.py test --settings config.settings.test --parallel --keepdb"

coverage: 

docker exec django bash -c "coverage run manage.py test --settings config.settings.test --keepdb && coverage html"

смотрим htmlcov/index.html


## Postgres DB Backup:
https://cookiecutter-django.readthedocs.io/en/latest/docker-postgres-backups.html

