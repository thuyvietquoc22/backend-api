from datetime import datetime, timedelta

from decorator import singleton
from decorator import signleton


@singleton
class TimerHelper:

    @staticmethod
    def get_time_ago(minute_ago: int) -> datetime:
        return datetime.now() - timedelta(minutes=minute_ago)
