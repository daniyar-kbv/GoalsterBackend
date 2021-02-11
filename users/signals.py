from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from users.models import Transaction, Profile, OTP
from main.tasks import send_email, delete_otp
from utils import emails, upload
from dateutil.relativedelta import relativedelta
import constants, datetime


@receiver(post_save, sender=Transaction)
def transaction_created(sender, instance, created=True, **kwargs):
    if created:
        user = instance.user
        user.is_premium = True
        user.save()


@receiver(pre_delete, sender=Profile)
def profile_pre_deleted(sender, instance, created=True, **kwargs):
    if instance.avatar:
        upload.delete_file(instance.avatar)


@receiver(post_save, sender=OTP)
def otp_saved(sender, instance, created=True, **kwargs):
    if created:
        after_day = datetime.datetime.now() + datetime.timedelta(days=1)
        delete_otp.apply_async(args=[instance.id], eta=after_day)