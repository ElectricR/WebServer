# Релевантные команды

* $ make start - запуск веб-сервера. Вначале создаётся compose.yaml, основывающийся на запрошенном количестве инстансов (параметр INSTANCE_COUNT в файле .env). Далее, после поднятия всех контейнеров, общение с сервером происходит через балансировщик, находящийся на порте, заданном в переменной BALANCER_PORT файла .env.
* $ make stop - остановка веб-сервера.
* $ make test - запуск тестов, описанных в test_server.py.
* $ make clean - удаление всех контейнеров, всех образов инстанса и балансировщика, всех образов с именем none, а также удаление compose.yaml.
* $ make healthcheck - проверка наличия docker, docker-compose, flake8, autopep8.
* $ make lint - проверка стандартизованности кода с помощью flake8.
* $ make autopep - автоисправление кода для соответствия стандарту с помощью autopep8
