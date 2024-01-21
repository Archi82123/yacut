**YaCut** — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.


Клонировать репозиторий и перейти в него в командной строке:

```
git clone <ссылка на репозиторий>

cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

Запустить приложение:

```
flask run
```

Откройте браузер и перейдите по адресу http://127.0.0.1:5000/

**Описание API**

1. Создание новой короткой ссылки
URL: /api/id/

Метод: POST

Тело запроса:

```
{
  "url": "длинная_ссылка",
  "custom_id": "пользовательская_короткая_ссылка" (необязательно)
}
```

2. Получение оригинальной ссылки по короткому идентификатору
URL: /api/id/<short_id>/

Метод: GET

Параметры запроса:

-short_id (обязательно): Короткий идентификатор ссылки.