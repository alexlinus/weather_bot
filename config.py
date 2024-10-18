import os

from sqlalchemy import URL

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", default="<some_token>")

# --- DATABASE SETTINGS --- #

url = URL.create(
    drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using (psycopg2)
    database=os.getenv("POSTGRES_DB"),
    port=os.getenv("POSTGRES_PORT", default=5432),
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
)

# --- Messages --- #

SUCCESSFUL_SUBSCRIPTION_MSG = os.getenv(
    "SUCCESSFUL_SUBSCRIPTION_MSG",
    default="<b>Привет, {user_name}</b>. <em>Вы успешно подписались на рассылку прогноза погоды!</em>",
)

SUBSCRIBER_ALREADY_EXIST_MSG = os.getenv(
    "SUCCESSFUL_SUBSCRIPTION_MSG",
    default=(
        "<b>Привет, {user_name}</b>. <em>Вы уже давно подписаны! "
        "Нет необходимости запускать команду start снова и снова.</em>"
    ),
)

FORECAST_MESSAGE_FORMAT_EVENING = os.getenv(
    "FORECAST_MESSAGE_FORMAT_EVENING",
    default="""
<b>Доброй ночи, {user_name}!</b> Вот тебе прогноз погоды на завтра в {city_name}е:
{tomorrow_temp}°C (min {tomorrow_min_temp}°C, max {tomorrow_max_temp}°C) ({tomorrow_weather_condition}), 
скорость ветра {tomorrow_wind_speed}.

Восход солнца: {sunrise_time}.
Заход солнца: {sunset_time}

Сейчас же за бортом:
{current_temp}°C ({current_weather_condition}), скорость ветра {current_wind_speed}.
"""
)

FORECAST_MESSAGE_FORMAT_MORNING = os.getenv(
    "FORECAST_MESSAGE_FORMAT_MORNING",
    default="""
<b>Доброе утро, {user_name}!</b> Вот тебе прогноз погоды на сегодня в {city_name}е:

Вас ожидает {today_temp}°C (min {today_min_temp}°C, max {today_max_temp}°C), 
{today_weather_condition}, скорость ветра {today_wind_speed}.

Заход солнца: {sunset_time}

Сейчас же за бортом:
{current_temp}°C ({current_weather_condition}), скорость ветра {current_wind_speed}.
"""
)

# --- API --
VISUAL_CROSSING_API_KEY = os.getenv("VISUAL_CROSSING_API_KEY", default="<some_key>>")

VISUAL_CROSSING_BASE_API_URL = os.getenv(
    "VISUAL_CROSSING_BASE_API_URL",
    default=(
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        "{city_name}/{from_date}/{to_date}?unitGroup=metric&include=days%2Ccurrent&key={api_key}&contentType=json"
    )
)

FORECAST_CITY_API_NAME = os.getenv("FORECAST_CITY_API_NAME", default="Bishkek")
FORECAST_CITY_NAME = os.getenv("FORECAST_CITY_NAME", default="Бишкек")
