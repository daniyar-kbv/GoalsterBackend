from django.db.models.signals import pre_delete
from django.dispatch import receiver
from celebrities.models import CelebrityProfile
from utils import upload


@receiver(pre_delete, sender=CelebrityProfile)
def profile_pre_deleted(sender, instance, created=True, **kwargs):
    if instance.avatar:
        upload.delete_file(instance.avatar)
