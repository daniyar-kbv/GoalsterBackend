from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from main.models import SelectedSphere, Observation, UserAnswer, Visualization, Help, Comment
from main.tasks import send_email, delete_emoton
from utils import emails, upload, time, notifications
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from PIL import Image
import datetime, constants


@receiver(post_save, sender=SelectedSphere)
def sphere_saved(sender, instance, created=True, **kwargs):
    if created:
        instance.expires_at = (instance.created_at + relativedelta(days=30))
        instance.save()


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
                    version = 1
                    if instance._request.path.__contains__('v2'):
                        version = 2
                    elif instance._request.path.__contains__('v3'):
                        version = 3
                    elif instance._request.path.__contains__('v4'):
                        version = 4
                    elif instance._request.path.__contains__('v5'):
                        version = 5
                    if version < 5:
                        body = emails.generate_observation_confirmation_email(
                            instance.observer.email,
                            'ru-ru' if instance.observer.language == constants.LANGUAGE_RUSSIAN else 'en-us',
                            version
                        )
                        send_email.delay(subject,
                                         body,
                                         instance.observer.email)
                    else:
                        send_email.delay(
                            subject,
                            emails.generate_observation_confirmation_email_v2(
                                instance._request,
                                'ru-ru' if instance.observer.language == constants.LANGUAGE_RUSSIAN else 'en-us'
                            ),
                            instance.observer.email,
                            html=True
                        )


@receiver(pre_delete, sender=Observation)
def observation_deleted(sender, instance, created=True, **kwargs):
    comments = Comment.objects.filter(goal=instance.goal)
    comments.delete()


@receiver(post_save, sender=UserAnswer)
def answer_saved(sender, instance, created=True, **kwargs):
    if created:
        after_day = datetime.datetime.now() + datetime.timedelta(days=1)
        delete_emoton.apply_async(args=[instance.id], eta=after_day)


@receiver(pre_delete, sender=Visualization)
def visualization_pre_deleted(sender, instance, created=True, **kwargs):
    if instance.image:
        upload.delete_folder(instance.image)


@receiver(post_save, sender=Help)
def help_saved(sender, instance, created=True, **kwargs):
    if created:
        send_email.delay(
            'Помощь GOALSTERS',
            f"""От: {instance.user.email}

{instance.text}

{instance.created_at.strftime(constants.DATETIME_FORMAT)}""",
            constants.HELP_RECIPIENT_EMAIL
        )
        instance.is_sent = True
        instance.save()


@receiver(post_save, sender=Comment)
def comment_saved(sender, instance, created=True, **kwargs):
    if created:
        data = {
            'type': constants.NOTIFICATION_COMMENT,
            'date': instance.goal.date.strftime(constants.DATE_FORMAT),
            'id': instance.goal.id
        }
        goal = instance.goal
        goal.is_new_comment = True
        goal.save()
        if instance.is_owner:
            try:
                observation = Observation.objects.get(goal=instance.goal)
            except:
                return
            if observation.observer.fcm_token:
                notifications.send_user_notification(
                    observation.observer,
                    constants.NEW_COMMENT_EN
                    if observation.observer.language == constants.LANGUAGE_ENGLISH else
                    constants.NEW_COMMENT_RU,
                    instance.text,
                    data
                )
        else:
            if instance.goal.user.fcm_token:
                notifications.send_user_notification(
                    instance.goal.user,
                    constants.NEW_COMMENT_EN
                    if instance.goal.user.language == constants.LANGUAGE_ENGLISH else
                    constants.NEW_COMMENT_RU,
                    instance.text,
                    data
                )