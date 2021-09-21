from django.db import models
from django.utils.translation import gettext_lazy as _
from utils import upload, validators
import constants


class Section(models.Model):
    name_en = models.CharField(f"{_('Name')} EN", max_length=100)
    name_ru = models.CharField(f"{_('Name')} RU", max_length=100)
    image = models.ImageField(
        _('Image'),
        upload_to=upload.knowledge_image_path,
        validators=[validators.validate_file_size, validators.basic_validate_images]
    )
    order = models.PositiveIntegerField(_('Order'), default=0, blank=False, null=False)
    is_active = models.BooleanField(_('Is active'), default=False)

    class Meta(object):
        ordering = ['order']
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.name_en

    def save(self, *args, **kwargs):
        try:
            this = Section.objects.get(id=self.id)
            if this.image != self.image:
                upload.delete_file(this.image)
        except:
            pass

        if self.id is None:
            saved_image = self.image
            self.image = None
            super(Section, self).save(*args, **kwargs)
            self.image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Section, self).save(*args, **kwargs)

    def get_name(self, language):
        if language == constants.LANGUAGE_ENGLISH:
            return self.name_en
        elif language == constants.LANGUAGE_RUSSIAN:
            return self.name_ru
        return None


class Story(models.Model):
    text_en = models.TextField(f"{_('Text')} EN")
    text_ru = models.TextField(f"{_('Text')} RU")
    image = models.ImageField(
        _('Image'),
        upload_to=upload.knowledge_story_image_path,
        validators=[validators.validate_file_size, validators.basic_validate_images]
    )
    link = models.URLField(_('URL'))
    order = models.PositiveIntegerField(_('Order'), default=0, blank=False, null=False)
    is_active = models.BooleanField(_('Is active'), default=False)

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        verbose_name=_('Section'),
        related_name='stories'
    )

    class Meta:
        ordering = ['order']
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')

    def __str__(self):
        return f'{self.section}: {self.title_en}'

    def save(self, *args, **kwargs):
        try:
            this = Story.objects.get(id=self.id)
            if this.image != self.image:
                upload.delete_file(this.image)
        except:
            pass

        if self.id is None:
            saved_image = self.image
            self.image = None
            super(Story, self).save(*args, **kwargs)
            self.image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Story, self).save(*args, **kwargs)

    def get_title(self, language):
        if language == constants.LANGUAGE_ENGLISH:
            return self.title_en
        elif language == constants.LANGUAGE_RUSSIAN:
            return self.title_ru
        return None

    def get_text(self, language):
        if language == constants.LANGUAGE_ENGLISH:
            return self.text_en
        elif language == constants.LANGUAGE_RUSSIAN:
            return self.text_ru
        return None