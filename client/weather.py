from __future__ import annotations

import dataclasses
import datetime
import logging

import requests
from telebot.apihelper import ApiTelegramException
from translate import Translator

import config
from db.queries import SubscriberQueryRepo
from main import session_pool, bot
from client.utils import get_dates, MessageType

logger = logging.getLogger(__name__)


def _build_api_url(
    city: str = config.FORECAST_CITY_NAME,
    from_date: datetime.date = None,
    to_date: datetime.date = None,
) -> str:
    """Function to build final API url."""
    url = config.VISUAL_CROSSING_BASE_API_URL.format(
        city_name=city,
        from_date=from_date,
        to_date=to_date,
        api_key=config.VISUAL_CROSSING_API_KEY,
    )
    return url


def _translate(translator: Translator, text_to_translate: str = "") -> str:
    """Shortcut to translate string to another language if not empty-string was passed."""
    if text_to_translate:
        return translator.translate(text_to_translate)
    return text_to_translate


@dataclasses.dataclass
class ForecastForDay:
    """Dataclass represents parsed forecast data for one entity (day, or current state of the weather)."""
    temp: int
    temp_feels_like: int

    forecast_date: datetime.date
    wind_speed: int

    temp_min: int | None = None
    temp_max: int | None = None

    conditions: str = ""
    conditions_description: str = ""

    sunset: str = ""
    sunrise: str = ""

    # if is_current_conditions is True,
    # that means temp_min, temp_max, conditions_description will be empty or 0.
    # no need to render in text message those values
    is_current_conditions: bool = False

    @classmethod
    def from_response(
        cls,
        data: dict,
        forecast_date: datetime.date,
        translator: Translator,
        is_current_conditions: bool = False,
    ) -> "ForecastForDay":
        """Shortcut to build dataclass instance from response data."""
        conditions = translator.translate(data.get("conditions", ""))
        return cls(
            temp=round(data.get("temp", 0)),
            temp_min=round(data.get("tempmin", 0)),
            temp_max=round(data.get("tempmax", 0)),
            temp_feels_like=round(data.get("feelslike", 0)),
            conditions=conditions,
            conditions_description=data.get("description", ""),
            sunset=data.get("sunset", ""),
            sunrise=data.get("sunrise", ""),
            wind_speed=data.get("windspeed", 0),
            forecast_date=forecast_date,
            is_current_conditions=is_current_conditions,
        )


@dataclasses.dataclass
class ParsedForecast:
    """Dataclass represents parsed forecast data.."""
    today: ForecastForDay
    tomorrow: ForecastForDay
    current: ForecastForDay

    city_name: str

    @classmethod
    def from_response(cls, data: dict) -> "ParsedForecast":
        """Shortcut to build dataclass instance from response data."""
        today, tomorrow = get_dates()
        forecast_by_days = {
            datetime.datetime.fromisoformat(item["datetime"]).date(): item for item in data["days"]
        }

        translator = Translator(from_lang="en", to_lang="ru")

        return cls(
            today=ForecastForDay.from_response(forecast_by_days[today], forecast_date=today, translator=translator),
            tomorrow=ForecastForDay.from_response(
                forecast_by_days[tomorrow],
                forecast_date=tomorrow,
                translator=translator,
            ),
            current=ForecastForDay.from_response(
                data=data["currentConditions"],
                forecast_date=today,
                is_current_conditions=True,
                translator=translator,
            ),
            city_name=config.FORECAST_CITY_NAME,
        )

    def to_user_msg(self, user_name: str, message_type: MessageType) -> str:
        """Convert parsed forecast data to text message, in order to send to the end-subscriber."""

        common_params = {
            "user_name": user_name,
            "city_name": self.city_name,
            "current_temp": self.current.temp,
            "current_weather_condition": self.current.conditions,
            "current_wind_speed" : self.current.wind_speed,
        }

        if message_type == MessageType.EVENING:
            message = config.FORECAST_MESSAGE_FORMAT_EVENING.format(
                **common_params,
                # tomorrow
                sunrise_time=self.tomorrow.sunrise,
                sunset_time=self.tomorrow.sunset,
                tomorrow_temp=self.tomorrow.temp,
                tomorrow_min_temp=self.tomorrow.temp_min,
                tomorrow_max_temp=self.tomorrow.temp_max,
                tomorrow_weather_condition=self.tomorrow.conditions,
                tomorrow_wind_speed=self.tomorrow.wind_speed,
            )
        else:
            message = config.FORECAST_MESSAGE_FORMAT_MORNING.format(
                **common_params,
                today_temp=self.today.temp,
                today_min_temp=self.today.temp_min,
                today_max_temp=self.today.temp_max,
                today_weather_condition=self.today.conditions,
                today_wind_speed=self.today.wind_speed,
                sunset_time=self.today.sunset,
            )
        return message


def fetch_forecast() -> ParsedForecast:
    """Entrypoint to fetch F"""
    today, tomorrow = get_dates()
    response = requests.get(_build_api_url(from_date=today, to_date=tomorrow))
    data = response.json()
    return ParsedForecast.from_response(data)


def send_forecast(message_type: MessageType) -> None:
    with session_pool() as session:
        subscribers = SubscriberQueryRepo(session=session).get_all_subscribers()

    parsed_forecast = fetch_forecast()
    for subscriber in subscribers:
        try:
            bot.send_message(
                chat_id=subscriber.telegram_id,
                text=parsed_forecast.to_user_msg(
                    user_name=subscriber.first_name,
                    message_type=message_type,
                ),
                parse_mode="html",
            )
        except ApiTelegramException as e:
            logger.error(
                "Error: Could not send forecast to Telegram user (%s): %s. Error: %s",
                str(subscriber.telegram_id),
                subscriber.first_name,
                e.description,
            )

