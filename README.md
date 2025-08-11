# Parser_MySklad

Данное приложение создано в целях получение информации с сервиса МойСклад. 
Для получение информации использовалось оффициальное API МойСклад

## Меню
- [Установка](#установка)

# Установка

1. Склонируйте репозиторий

```
git clone https://github.com/Ilyas-12345/Parser_MySklad.git
```

2. Создайте .venv и установите зависимости 

```
python3 .venv venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Создайте файл .env для переменных сред
> [!TIP]
> Пример заполнения .env файла:
> login=логин_аккаунта_мойсклад
> password=пароль_аккаунта_мойсклад
> DB_HOST=хост_бд
> DB_PORT=порт_бд
> DB_NAME=имя_бд
> DB_USER=юзер_бд
> DB_PASS=пароль_бд

4. Примените миграцию для создания таблиц БД

```
alembic -c migration/alembic.ini upgrade head
```

