from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from users.models import UserActivation, Transaction
from main.tasks import send_email, deactivate_premium
from utils import emails
from dateutil.relativedelta import relativedelta
import constants, datetime


@receiver(post_save, sender=UserActivation)
def activation_created(sender, instance, created=True, **kwargs):
    if instance:
        attrs_needed = ['_request', '_created']
        if all(hasattr(instance, attr) for attr in attrs_needed):
            if instance._created:
                send_email.delay(constants.ACTIVATION_EMAIL_SUBJECT,
                                 emails.generate_activation_email(instance.email, request=instance._request),
                                 instance.email)


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
        deactivate_premium.apply_async(args=[instance.user.id, instance.id], eta=eta)
