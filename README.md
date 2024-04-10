<h1 align="center">Тестовое задание</h1>
<h4 align="center">Стек: Django 4, DRF 3. А также используются асинхроные запросы browser API.</h4>
<small>Детальнее см requirements.txt</small>

![Тз](https://github.com/filthps/test-work03.2024/blob/master/images/task.png?raw=true)

<h2>Определение масштаба задачи, выбор стека</h2>
После ознакомления с рекомендуемой в задаче ссылкой на "матчасть" (анализ предметной области: - TF-IDF — статистическая мера),
  понимая особенности работы в рамках хранимых процедур субд, было решено производить все рассчёты на уровне СУБД. Django ORM обладает достаточной гибкостью для реализации сложных запросов как через JOIN, 
  так и через подзапрос (для связи между сущностями ТЕКСТ - СЛОВО), а также, при помощи метода FUNC, произвести вычисление логарифма на уровне СУБД.
  Оговорюсь сразу, что данное решение не взвешивалось детально и вряд ли является хорошим в услових реальных нагрузок.
  Первоначально была предпринята попытка реализации на чистом SQL

* Select из базы через **INNER JOIN**
![Запрос с использованием join](https://github.com/filthps/test-work03.2024/blob/master/images/2.png?raw=true)

* Select из базы через дополнительные select внутри главного select
![Запрос с использованием join](https://github.com/filthps/test-work03.2024/blob/master/images/2.1.png?raw=true)

![Запрос с использованием подзапросов](https://github.com/filthps/test-work03.2024/blob/master/images/3.png?raw=true)

![orm](https://github.com/filthps/test-work03.2024/blob/master/images/orm.png?raw=true)


<h2>Инициализация проекта, виртуального окружения Python, установка requirements</h2>

![setup](https://github.com/filthps/test-work03.2024/blob/master/images/startapp5.png?raw=true)

![setup](https://github.com/filthps/test-work03.2024/blob/master/images/startapp.png?raw=true)

![setup](https://github.com/filthps/test-work03.2024/blob/master/images/startapp1.png?raw=true)

![setup](https://github.com/filthps/test-work03.2024/blob/master/images/startapp2.png?raw=true)

![setup](https://github.com/filthps/test-work03.2024/blob/master/images/startapp3.png?raw=true)

![setup](https://github.com/filthps/test-work03.2024/blob/master/images/startapp4.png?raw=true)


<h2>Особенности конфигурации</h2>

* прошу обратить внимание на следующий момент: всего предусмотрено 3 разных варианта для взамодействия.
* В файлах form.js и settings.js модуля api можно ознакомиться подробнее:
![settings.js](https://github.com/filthps/test-work03.2024/blob/master/images/4.png?raw=true)


<h2>Запуск</h2>

![form](https://github.com/filthps/test-work03.2024/blob/master/images/1.png?raw=true)

![table](https://github.com/filthps/test-work03.2024/blob/master/images/test1.png?raw=true)


