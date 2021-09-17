from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CelebritiesConfig(AppConfig):
    name = 'celebrities'
    verbose_name = _('Celebrities')

    def ready(self):
        import celebrities.signals
