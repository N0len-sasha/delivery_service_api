# Установка 
## Как развернуть проект на локальной машине 
### Клонировать репозиторий и перейти в него в командной строке 
``` 
  git clone https://github.com/N0len-sasha/delivery_service_api.git
``` 
``` 
  cd delivery_service_api
``` 

### Установить зависимости 
``` 
  pip install poetry 
``` 
``` 
  poetry install
``` 
### Выполнить миграции
```
alembic init
```
```
alembic revision --autogenerate -m "init"

```
```
alembic upgrade head
```
### Создать файл .env
```
REDIS_HOST=value
REDIS_PORT=value
REDIS_DB=value
REDIS_KEY=value
REDIS_TTL=value
TIMEZONE="value"
URL_PATH="https://www.cbr-xml-daily.ru/daily_json.js"
```
### Запустить проект 
``` 
  docker-compose docker-compose-local.yaml up -d
  Pycharm (Shift + F10) 
``` 

# Основные запросы
## Documentation Swagger
```http://localhost:8000/docs/```
## Register & Login
### ```POST http://localhost:8000/api_v1/register/```
### Тело:
```
{
    "username": "Oleg"
}
```
### Ответ:
```
{
    "username": "Oleg"
}
```
### ```POST http://localhost:8000/api_v1/login/```
### Тело:
```
{
    "username": "Oleg"
}
```
### Ответ:
```
{
    "username": "Oleg",
    "id": 3
}
```
## Packages
### ```GET http://localhost:8000/api_v1/packages/```
### ```GET http://localhost:8000/api_v1/packages/?page=1&size=2 (пагинация)``` 
### ```GET http://localhost:8000/api_v1/packages/?type=Clothing (фильтрация по полю type)```
### ```GET http://localhost:8000/api_v1/packages/?has_price=0 ((фильтрация по тому, если цена (1) или нет (0)))```
### ```GET http://localhost:8000/api_v1/packages/1/ ```
### ```POST http://localhost:8000/api_v1/packages/```
### Тело:
```
{
  "name": "111",
  "weight": 78,
  "price": 120,
  "type_id": 2
}
```
### Ответ:
```
{
    "username": "Oleg",
    "id": 3
}
```
## Types
### ```GET http://localhost:8000/api_v1/types/```
### Ответ
```
[
    {
        "id": 1,
        "name": "Electronics"
    },
    {
        "id": 2,
        "name": "Clothing"
    },
    {
        "id": 3,
        "name": "Others"
    }
]
```
## Автор 
Платошин Александр Игоревич 
