from django.conf import settings
from django.utils import timezone
import pytz, datetime


# def convert_datetime_to_local


def get_local_dt():
    server_tz = pytz.timezone(settings.TIME_ZONE)
    server = server_tz.localize(datetime.datetime.now())
    local_tz = timezone.get_current_timezone()
    return local_tz.normalize(server.astimezone(local_tz))
