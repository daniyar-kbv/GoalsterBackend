from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KnowledgeConfig(AppConfig):
    name = 'knowledge'
    verbose_name = _('Knowledge')

    def ready(self):
        import knowledge.signals
