import enum
from collections import namedtuple
from datetime import datetime, timedelta
import pytz

ForecastDates = namedtuple("ForecastDates", ["today", "tomorrow"])

TZ = pytz.timezone("Asia/Bishkek")


class MessageType(enum.IntEnum):
    EVENING = 1
    MORNING = 2


def get_dates() -> ForecastDates:
    """Shortcut to get needed dates for our forecast."""
    gmt6_time = datetime.now(tz=TZ).date()
    return ForecastDates(today=gmt6_time, tomorrow=gmt6_time + timedelta(days=1))