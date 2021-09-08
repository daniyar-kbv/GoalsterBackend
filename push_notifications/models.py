from django.db import models, connection
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from firebase_admin import messaging
from helper.models import Weekday
from utils import types
import constants


class NonCustomizableNotificationType(models.Model):
    type = models.PositiveSmallIntegerField(_('Type'), choices=constants.NON_CUSTOMIZABLE_NOTIFICATION_TYPES)
    title_en = models.CharField(f"{_('Title')} EN", max_length=100)
    title_ru = models.CharField(f"{_('Title')} RU", max_length=100)
    body_en = models.TextField(f"{_('Body')} EN", null=True, blank=True)
    body_ru = models.TextField(f"{_('Body')} EN", null=True, blank=True)

    class Meta:
        verbose_name = _('Non customizable notification type')
        verbose_name_plural = _('Non customizable notification types')

    def __str__(self):
        return types.get_type_value(constants.NON_CUSTOMIZABLE_NOTIFICATION_TYPES, self.type)


class PeriodicNotification(models.Model):
    title_en = models.CharField(f"{_('Title')} EN", max_length=100)
    title_ru = models.CharField(f"{_('Title')} RU", max_length=100)
    body_en = models.TextField(f"{_('Body')} EN", null=True, blank=True)
    body_ru = models.TextField(f"{_('Body')} EN", null=True, blank=True)
    weekdays = models.ManyToManyField(
        Weekday,
        related_name='notification_types',
        verbose_name=_('Weekday')
    )
    time = models.TimeField(_('Time'))

    class Meta:
        verbose_name = _('Periodic notification')
        verbose_name_plural = _('Periodic notifications')

    def __str__(self):
        return self.title_en


class DisposableNotification(models.Model):
    title_en = models.CharField(f"{_('Title')} EN", max_length=100)
    title_ru = models.CharField(f"{_('Title')} RU", max_length=100)
    body_en = models.TextField(f"{_('Body')} EN", null=True, blank=True)
    body_ru = models.TextField(f"{_('Body')} EN", null=True, blank=True)

    class Meta:
        verbose_name = _('Disposable notification')
        verbose_name_plural = _('Disposable notification')

    def __str__(self):
        return self.title_en

    def send(self):
        messages = [
            messaging.Message(
                notification=messaging.Notification(
                    title=self.title_en,
                    body=self.body_en
                ),
                topic=constants.TOPIC_EN,
            ),
            messaging.Message(
                notification=messaging.Notification(
                    title=self.title_ru,
                    body=self.body_ru
                ),
                topic=constants.TOPIC_RU,
            )
        ]
        messaging.send_all(messages)


if 'push_notifications_noncustomizablenotificationtype' in connection.introspection.table_names():
    for index, type in enumerate(constants.NON_CUSTOMIZABLE_NOTIFICATION_TYPES):
        try:
            NonCustomizableNotificationType.objects.get(type=type[0])
        except:
            obj: NonCustomizableNotificationType = NonCustomizableNotificationType.objects.create(
                type=type[0],
                title_en=types.get_type_value(
                    constants.NON_CUSTOMIZABLE_NOTIFICATION_TITLES_EN,
                    type[0]
                ),
                title_ru=types.get_type_value(
                    constants.NON_CUSTOMIZABLE_NOTIFICATION_TITLES_RU,
                    type[0]
                ),
                body_en=types.get_type_value(
                    constants.NON_CUSTOMIZABLE_NOTIFICATION_BODIES_EN,
                    type[0]
                ),
                body_ru=types.get_type_value(
                    constants.NON_CUSTOMIZABLE_NOTIFICATION_BODIES_RU,
                    type[0]
                ),
            )
