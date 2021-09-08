from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from celery.app import control
from push_notifications.models import DisposableNotification


@receiver(post_save, sender=DisposableNotification)
def disposable_notification_saved(sender, instance: DisposableNotification, created=True, **kwargs):
    instance.send()