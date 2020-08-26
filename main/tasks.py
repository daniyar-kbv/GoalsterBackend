from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from users.models import MainUser
from main.models import SelectedSphere, UserAnswer
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
        print(settings.EMAIL_HOST_USER)
        print(e)
        logger.info(f'Task: Email sending to {to} failed {print(e) if count == 0 else ""}')
        send_email(subject, body, to, attachments, count=count+1)


@shared_task
def reset_spheres(sphere_id):
    try:
        sphere = SelectedSphere.objects.get(id=sphere_id)
    except:
        return
    sphere.delete()
#     TODO: Notification


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
        pass
    # TODO: notifucation


@shared_task
def notify_before(user_id):
    try:
        user = MainUser.objects.get(id=user_id)
    except:
        return
    # TODO: Notification