# donstu_helper

Простой веб-сервис с помощью которого вы сможете интегрировать в свое приложение, сайт или чат-бот возможность пользователям получать данные из API ДГТУ с помощью текстовых или голосовых сообщений

На данный момент реализован анализ следующих запросов:

- Расписание на сегодня
- Расписание на завтра
- Сводная успеваемость
- ...

(Список будет пополняться)

**Для запуска сервиса используйте файл `start.bat`. Не забудьте поменять параметры под себя.**


# Использование

На данный момент сервис нигде не хостится

## Авторизация

Для запросов на сервис необходимо получить JWT токен API ДГТУ. Сделать это можно несколькими способами:

- `POST https://edu.donstu.ru/api/tokenauth` со следующим json-телом:
  
    ```json
    {
        "userName": "почта",
        "password": "пароль",
        "isParent": false,
        "fingerprint": ""
    }
    ```
- `POST https://lk.donstu.ru/api/tokenauth` со следующим json-телом:
  
    ```json
    {
        "userName": "почта",
        "password": "пароль"
    }
    ```

После получения токена вы можете хранить его на устройстве и использовать в течении недели, способов продления токена, кроме как с помощью повторной авторизации, вроде как нет.

**При запросах на сервис поместите токен в хедер `Authorization`**


## Запрос

На данный момент сервис принимает два типа запросов:
- `POST ../analyze_audio` - анализ голосовых сообщений

  Поместите в тело запроса бинарное представление звукового файла одного из следующих расширений: `mp4, mp3, wav, wave, ogg`

- `POST ../analyze_text` - анализ текстовых сообщений:

  Поместите в тело запроса json следующей структуры:

  ```json
  {
      "text": "ваш текст"
  }
  ```

### Что стоит учитывать при запросе?
- Так как мы не смогли найти корпус размеченных текстовых данных, для анализа текста мы используем простой метод на основе опорных векторов. В следствие чего, крайне не рекомендуется отправлять длинные сложные запросы
- Сервис имеет ограничения на количество символов в тексте запроса (по умолчанию 100) и вес тела запроса (по умолчанию 40 МБ)


## Ответ

При любом запросе сервис будет присылать в качестве ответа json следующей структуры:

```json
{
    "is_success": "успешен запрос или нет - true или false",
    "message": "сообщение сервера",
    "data": {
        "type": "тип запроса",
        "data": [ "ваши данные" ]
    }
}
```

### Что учитывать при десериализации?
- Поле `"message"` может быть пустым (`nullable`), если запрос был успешен и сервису не надо сообщать об ошибках
- Поле `"data"` может быть пустым (`nullable`), если запрос не был успешен, в случае успеха возвращает список объектов, структура которых зависит от запроса
- Поле `"data" -> "type"` содержит тип запроса который распознал сервис:
  + `"rasp_today"` - пары на сегодня
  + `"rasp_tomorrow"` - пары на завтра
  + `"marks"` - сводная успеваемость

# Что дальше?
- Данные для векторизации будут перенесенны в БД из простого Excel (простите, времени не хватило) 
- Переход на WSGI (тоже времени не хватило)
- Использование более совершенного метода анализа текста (например, предобученные лингвистические модели)
- Добавление защиты от DDOS
- ...
  
