# kpoisk_parser
<strong>Парсер рейтинга 250 Кинопоиска</strong>
<br>

Чтобы запустить нужно:
1. Дублировать файл .env_example и назвать копию .env
Там прописать доступ к вашей БД на postgreSQL

Зайти на кинопоиск, скопировать из хидеров оттуда значение параметра cookie, прописать в параметр COOKIE в енве
2. Выполнить миграции:
python .\manage.py migrate

3. Создать суперюзера:
python .\manage.py createsuperuser --username=parser_admin
Указать пароль и email (если попросит)


<strong>Далее можно запустить с помощью python shell:</strong>

Для вывода данных в формате CSV:

<em>python .\manage.py parse_250 --file_format=csv</em>

Для вывода данных в формате XLSX:

<em>python .\manage.py parse_250 --file_format=xlsx</em>

Полученный файл появится в папке с проектом под названиями top250.csv и top250.xlsx соответственно
Также данные запишутся в базу в таблицу Movies