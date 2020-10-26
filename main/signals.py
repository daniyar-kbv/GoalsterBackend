from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from main.models import SelectedSphere, Observation, UserAnswer, Visualization, Help
from main.tasks import reset_spheres, send_email, delete_emoton, notify_before
from utils import emails, upload, time
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from PIL import Image
import datetime, constants


@receiver(post_save, sender=SelectedSphere)
def sphere_saved(sender, instance, created=True, **kwargs):
    if created:
        instance.expires_at = (instance.created_at + relativedelta(days=30))
        instance.save()
        if SelectedSphere.objects.filter(user=instance.user).count() == 1:
            reset_spheres.apply_async(args=[instance.user.id], eta=instance.expires_at)
            notify_before.apply_async(args=[instance.user.id], eta=instance.expires_at - datetime.timedelta(days=3))


@receiver(post_save, sender=Observation)
def observation_saved(sender, instance, created=True, **kwargs):
    if instance:
        if created:
            instance.observed = instance.goal.user
            if Observation.objects.filter(observed=instance.goal.user, observer=instance.observer, is_confirmed=True).count() > 0:
                instance.is_confirmed = True
            instance.save()
        attrs_needed = ['_request', '_created']
        if all(hasattr(instance, attr) for attr in attrs_needed):
            if instance._created:
                if Observation.objects.filter(observed=instance.observed, observer=instance.observer).count() == 1:
                    if instance.observer.language == constants.LANGUAGE_RUSSIAN:
                        subject = constants.OBSERVATION_EMAIL_SUBJECT_RU
                    else:
                        subject = constants.OBSERVATION_EMAIL_SUBJECT_EN
                    if instance._request.path.__contains__('v2'):
                        body = emails.generate_observation_confirmation_email_v2(
                                         instance.observer.email,
                                         'ru-ru' if instance.observer.language == constants.LANGUAGE_RUSSIAN else 'en-us'
                                     )
                    elif instance._request.path.__contains__('v3'):
                        body = emails.generate_observation_confirmation_email_v3(
                                         instance.observer.email,
                                         'ru-ru' if instance.observer.language == constants.LANGUAGE_RUSSIAN else 'en-us'
                                     )
                    else:
                        body = emails.generate_observation_confirmation_email(
                            instance.observer.email,
                            'ru-ru' if instance.observer.language == constants.LANGUAGE_RUSSIAN else 'en-us'
                        )
                    send_email.delay(subject,
                                     body,
                                     instance.observer.email)


@receiver(post_save, sender=UserAnswer)
def answer_saved(sender, instance, created=True, **kwargs):
    if created:
        next_day = time.get_local_dt() + datetime.timedelta(days=1)
        next_day_start = next_day.replace(hour=0, minute=0, second=0)
        delete_emoton.apply_async(args=[instance.id], eta=next_day_start)


@receiver(pre_delete, sender=Visualization)
def visualization_pre_deleted(sender, instance, created=True, **kwargs):
    if instance.image:
        upload.delete_folder(instance.image)


# @receiver(post_save, sender=Help)
# def help_saved(sender, instance, created=True, **kwargs):
#     if created:
#         sent = send_email(
#             'Помощь GOALSTERS',
#             f"""От: {instance.user.email}
#
# {instance.text}
#
# {instance.created_at.strftime(constants.DATETIME_FORMAT)}""",
#             constants.HELP_RECIPIENT_EMAIL
#         )
#         instance.is_sent = sent
#         instance.save()
