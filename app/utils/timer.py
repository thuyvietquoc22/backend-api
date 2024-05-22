from datetime import datetime, timedelta

from app.decorator import singleton


@singleton
class TimerHelper:

    @staticmethod
    def get_time_ago(minute_ago: int) -> datetime:
        return datetime.now() - timedelta(minutes=minute_ago)
