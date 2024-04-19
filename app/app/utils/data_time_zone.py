from datetime import datetime

import pytz


class DateTimeColombia:
    BOGOTA_TZ = pytz.timezone("America/Bogota")

    @staticmethod
    def now():
        return datetime.now(DateTimeColombia.BOGOTA_TZ)

    @staticmethod
    def today():
        return datetime.now(DateTimeColombia.BOGOTA_TZ).date()


if __name__ == "__main__":
    print(DateTimeColombia.now())
    print(DateTimeColombia.today())
