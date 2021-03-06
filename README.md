Backend на Python Django Rest Framework

Реализованная функциональность:

1. Запрос на получение списка всех показателей KPI со значениями за последнией день.
2. Запрос на получение значений конкретного показателя за определённый промежуток (неделя, месяц)
3. Запрос на определение проблем с загруженностью складов по дате.

Особенность проекта в следующем:

1. Автоматическое определение резких изменений в значений показателя KPI (по стандартному отклонению предыдущих значений)
2. Анализ данных для выявлений проблем с загруженностью агрегатов. В частности, определение недостаточно заполненных складов до агрегата или переполненных после. Представление информации в удобной, читаемой форме.

Основной стек технологий:

1. Python Django Rest Framework
2. Postgresql
3. Docker, Nginx

Демо

развёрнут на https://e-kondr01.ru

Для локального запуска:

docker-compose -f local.yml up --build --force-recreate

docker exec accenture_django bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py loaddata kpi_stats.json""


Документация запросов в коллекции Postman в файле requests.postman_collection.json

Разработчики

Кондрашов Егор, tg: @e_kondr01

Код для определения проблем в заполненности складов - Александр Лакиза, tg: @alexanderlakiza
