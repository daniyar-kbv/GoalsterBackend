from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from main.models import SelectedSphere, Observation, UserAnswer, Visualization
from main.tasks import reset_spheres, send_email, delete_emoton, notify_before
from utils import emails, upload
from dateutil.relativedelta import relativedelta
from PIL import Image
import datetime


@receiver(post_save, sender=SelectedSphere)
def sphere_saved(sender, instance, created=True, **kwargs):
    if created:
        instance.expires_at = (instance.created_at + relativedelta(days=30)).replace(hour=0, minute=0, second=0)
        instance.save()
        reset_spheres.apply_async(args=[instance.id], eta=instance.expires_at)
        notify_before.apply_async(args=[instance.id], eta=instance.expires_at - datetime.timedelta(days=3))


@receiver(post_save, sender=Observation)
def observation_saved(sender, instance, created=True, **kwargs):
    if instance:
        if created:
            instance.observed = instance.goal.user
            instance.save()
        attrs_needed = ['_request', '_created']
        if all(hasattr(instance, attr) for attr in attrs_needed):
            if instance._created:
                pass
                # TODO: finish email sending
                # send_email.delay('asd',
                #                  emails.generate_observation_confirmation_email(instance.email, request=instance._request),
                #                  instance.email)


@receiver(post_save, sender=UserAnswer)
def answer_saved(sender, instance, created=True, **kwargs):
    if created:
        next_day = instance.created_at + datetime.timedelta(minutes=1)
        next_day_start = next_day.replace(hour=0, minute=0, second=0)
        delete_emoton.apply_async(args=[instance.id], eta=next_day_start)


@receiver(pre_delete, sender=Visualization)
def visualization_pre_deleted(sender, instance, created=True, **kwargs):
    if instance.image:
        upload.delete_folder(instance.image)


# @receiver(post_save, sender=Visualization)
# def visualization_post_save(sender, instance, created=True, **kwargs):
#     if created:
#         print(instance.image.path)
