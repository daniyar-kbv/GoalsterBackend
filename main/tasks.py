from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from users.models import MainUser
from main.models import SelectedSphere, UserAnswer, UserResults, Goal
from utils.notifications import send_notification
import os
import logging, constants

logger = logging.getLogger(__name__)


@shared_task
def send_email(subject, body, to, attachments=None, count=0):
    logger.info(f'Task: Email sending to {to} started')
    if count == 10:
        return
    try:
        email = EmailMessage(
            subject,
            body,
            from_email=os.environ['EMAIL_HOST_USER'],
            to=[to]
        )
        if attachments:
            email.attach_file(attachments)
        email.send()
        logger.info(f'Task: Email sending to {to} finished')
    except Exception as e:
        logger.info(f'Task: Email sending to {to} failed {print(e) if count == 0 else ""}')
        send_email(subject, body, to, attachments, count=count+1)


@shared_task
def reset_spheres(user_id):
    try:
        user = MainUser.objects.get(id=user_id)
    except:
        return
    spheres = SelectedSphere.objects.filter(user=user)
    existing_results = UserResults.objects.filter(user=user)
    existing_results.delete()
    for sphere in spheres:
        UserResults.objects.create(user=user,
                                   sphere_name=sphere.sphere,
                                   number=Goal.objects.filter(user=user, sphere=sphere, is_done=True).count())
    spheres.delete()
    send_notification(user.fcm_token, constants.NOTIFICATION_END)


@shared_task
def delete_emoton(answer_id):
    try:
        answer = UserAnswer.objects.get(id=answer_id)
    except:
        return
    answer.delete()


@shared_task
def after_three_days(user_id):
    try:
        user = MainUser.objects.get(id=user_id)
    except:
        return
    delta = timezone.now() - user.last_activity
    if delta.days >= 3:
        send_notification(user.fcm_token, constants.NOTIFICATION_3DAYS)


@shared_task
def notify_before(user_id):
    try:
        user = MainUser.objects.get(id=user_id)
    except:
        return
    send_notification(user.fcm_token, constants.NOTIFICATION_BEFORE_END)


@shared_task
def deactivate_premium(user_id):
    try:
        user = MainUser.objects.get(id=user_id)
    except:
        return
    user.is_premium = False
    user.save()
