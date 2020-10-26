from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from users.models import Transaction
from main.tasks import send_email
from utils import emails
from dateutil.relativedelta import relativedelta
import constants, datetime


@receiver(post_save, sender=Transaction)
def transaction_created(sender, instance, created=True, **kwargs):
    if created:
        user = instance.user
        user.is_premium = True
        user.save()
        if instance.time_unit == constants.MONTH:
            eta = datetime.datetime.now() + relativedelta(months=instance.time_amount)
        elif instance.time_unit == constants.YEAR:
            eta = datetime.datetime.now() + relativedelta(years=instance.time_amount)
