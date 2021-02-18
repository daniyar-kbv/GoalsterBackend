from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.utils import timezone
from django.conf import settings
from users.models import MainUser, Transaction, OTP
from main.models import SelectedSphere, UserAnswer, UserResults, Goal
from utils.notifications import send_notification, get_topic_text
from dateutil.relativedelta import relativedelta
import os
import logging, constants, datetime, requests

logger = logging.getLogger(__name__)


@shared_task
def send_email(subject, body, to, attachments=None, html=False, count=0):
    logger.info(f'Task: Email sending to {to} started')
    if count == 10:
        return False
    try:
        email = EmailMessage(
            subject,
            body,
            from_email=os.environ['EMAIL_HOST_USER'],
            to=[to]
        )
        if attachments:
            for attachment in attachments:
                email.attach_file(attachment)
        if html:
            email.content_subtype = 'html'
        email.send()
        logger.info(f'Task: Email sending to {to} finished')
        return True
    except Exception as e:
        logger.info(f'Task: Email sending to {to} failed {print(e) if count == 0 else ""}')
        return send_email(subject, body, to, attachments, html, count=count+1)


@shared_task
def check_reset_spheres():
    for user in MainUser.objects.all():
        sphere = SelectedSphere.objects.filter(user=user).first()
        if sphere:
            if sphere.expires_at.date() <= datetime.date.today():
                spheres = SelectedSphere.objects.filter(user=user)
                existing_results = UserResults.objects.filter(user=user)
                existing_results.delete()
                for sphere in spheres:
                    UserResults.objects.create(user=user,
                                               sphere_name=sphere.sphere,
                                               number=Goal.objects.filter(user=user, sphere=sphere, is_done=True).count())
                spheres.delete()
                send_notification(user, constants.NOTIFICATION_END)
                user.show_results = True
            elif sphere.expires_at.date() == datetime.date.today() - datetime.timedelta(days=3):
                send_notification(user, constants.NOTIFICATION_BEFORE_END)


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
    if delta.days >= 3 and not user.received_three_days_notification:
        send_notification(user, constants.NOTIFICATION_3DAYS)
        user.received_three_days_notification = True
        user.save()


@shared_task
def check_premium():
    for user in MainUser.objects.all():
        if user.is_premium:
            last_transaction = Transaction.objects.filter(user=user).order_by('-created_at').first()
            if last_transaction:
                if last_transaction.product_id == constants.PURCHASE_ONE_MONTH \
                and relativedelta(datetime.date.today(), last_transaction.created_at.date()).months > 0:
                    user.is_premium = False
                    user.save()
                elif last_transaction.product_id == constants.PURCHASE_THREE_MONTH \
                and relativedelta(datetime.date.today(), last_transaction.created_at.date()).months > 2:
                    user.is_premium = False
                    user.save()
                elif last_transaction.product_id == constants.PURCHASE_SIX_MONTH \
                and relativedelta(datetime.date.today(), last_transaction.created_at.date()).months > 5:
                    user.is_premium = False
                    user.save()
                elif last_transaction.product_id == constants.PURCHASE_ONE_YEAR \
                and relativedelta(datetime.date.today(), last_transaction.created_at.date()).years > 0:
                    user.is_premium = False
                    user.save()


@shared_task
def backup():
    call_command('dbbackup', '-c')
    call_command('mediabackup', '-c')
    os.system(f'cd backups && \
              git config --global user.email "{os.environ.get("GITHUB_EMAIL")}" && \
              git config --global user.name "{os.environ.get("GITHUB_USERNAME")}" && \
              git add . && \
              git commit -m "backup" && \
              git push https://{os.environ.get("GITHUB_USERNAME")}:{os.environ.get("GITHUB_PASSWORD")}@github.com/goalster/{os.environ.get("GITHUB_REPOSITORY")}.git --all')


@shared_task
def delete_otp(id):
    try:
        otp = OTP.objects.get(id=id)
    except:
        return
    otp.delete()