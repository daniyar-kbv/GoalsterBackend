import pytz

from django.utils import timezone
from django.contrib.auth.models import AnonymousUser


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.headers.get('Timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        if request.headers.get('FCM') and not isinstance(request.user, AnonymousUser):
            user = request.user
            user.fcm_token = request.headers.get('FCM')
            user.save()
        return self.get_response(request)
