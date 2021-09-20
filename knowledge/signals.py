from django.db.models.signals import pre_delete
from django.dispatch import receiver
from knowledge.models import Section, Story
from utils import upload


@receiver(pre_delete, sender=Section)
def section_pre_delete(sender, instance: Section, created=True, **kwargs):
    upload.delete_file(instance.image)


@receiver(pre_delete, sender=Story)
def story_pre_delete(sender, instance: Story, created=True, **kwargs):
    upload.delete_file(instance.image)
