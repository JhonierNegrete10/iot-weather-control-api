import pytz
from datetime import datetime
BOGOTA_TZ = pytz.timezone("America/Bogota")


def cotnow():
    return datetime.now(tz=BOGOTA_TZ)
