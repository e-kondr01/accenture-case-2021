# Цифровой прорыв, Accenture hack
Backend на Python Django Rest Framework

развёрнут на https://e-kondr01.ru

для локального деплоя:

docker-compose -f local.yml up --build --force-recreate

docker exec accenture_django bash -c "python manage.py makemigrations && python manage.py migrate""


Документация запросов в коллекции Postman в файле requests.postman_collection.json

Кондрашов Егор, 2021.

Код для определения проблем в заполненности складов - Александр Лакиза.
