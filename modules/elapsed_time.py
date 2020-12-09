from datetime import datetime


class ElapsedTime:
    def __init__(self, start: datetime, end: datetime) -> None:
        self.sec = int((end - start).total_seconds())

    def generate_hhmm(self) -> str:
        return ":".join([str(x).zfill(2) for x in [self.minutes, self.seconds]])

    def is_over_10_minute(self) -> bool:
        return self.minutes > 9

    @property
    def minutes(self) -> int:
        return int(self.sec // 60)

    @property
    def seconds(self) -> int:
        return int(self.sec % 60)
