import os

from huey import RedisHuey
from huey import crontab

from client.utils import MessageType
from client.weather import send_forecast

huey = RedisHuey("weather_bot", host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0)

RETRY_DELAY_SECONDS = 360  # 5 minutes
RETRY_COUNT = 2


# 3 PM  UTC time = 9 PM GMT+6
@huey.periodic_task(crontab(hour=15, minute=0), retries=RETRY_COUNT, retry_delay=RETRY_DELAY_SECONDS)
def evening_forecast():
    send_forecast(message_type=MessageType.EVENING)


# 4 AM UTC time = 10 AM GMT+6
@huey.periodic_task(crontab(hour=4, minute=0), retries=RETRY_COUNT, retry_delay=RETRY_DELAY_SECONDS)
def morning_forecast():
    send_forecast(message_type=MessageType.MORNING)