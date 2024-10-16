Used the following library

```python
poetry add pyTelegramBotAPI
```


# Получение разных типов данных (например фото)
```python
@bot.message_handler(content_types=["photo"])
```


# Ответ на сообщения

```python
    bot.reply_to(message, f"I don't understand you!")
```




### NOTES:
- sqlite - в python имеет встроенную поддержку (модуль sqlite3)





What is used here:
- https://huey.readthedocs.io/en/latest/installation.html



## Чтобы увидеть прогресс логи
```shell
docker-compose build --progress=plain --no-cache
```


## NOTES

- Когда мы передаем хосты внутри контейнеров, нужно оперировать не localhost, а названием сервиса в dockercompose или имя контейнера.
- `url = url.render_as_string(hide_password=False)` - обязательно hide_password должно быть False.