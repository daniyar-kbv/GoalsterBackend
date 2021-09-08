from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificationsConfig(AppConfig):
    name = 'push_notifications'
    verbose_name = _('Push notifications')

    def ready(self):
        import push_notifications.signals