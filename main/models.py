from django.utils.translation import gettext_lazy as _
from django.db import models, connection
from users.models import MainUser
from utils import upload, validators, types
from PIL import Image, ExifTags
import constants


class SelectedSphere(models.Model):
    description = models.TextField(_('Description'))
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)
    expires_at = models.DateTimeField(_('Expiration date'), blank=True, null=True)
    sphere = models.CharField(_('Sphere'), max_length=100)
    user = models.ForeignKey(MainUser,
                             on_delete=models.CASCADE,
                             related_name='selected',
                             verbose_name=_('User'))

    class Meta:
        verbose_name = _('Selected sphere')
        verbose_name_plural = _('Selected spheres')

    def __str__(self):
        return f'{self.id}: {self.user}, {self.sphere}'


class Goal(models.Model):
    name = models.TextField(_('Name'))
    date = models.DateField(_('Date'))
    time = models.PositiveSmallIntegerField(_('Time of the day'),
                                            choices=constants.TIME_TYPES,
                                            default=constants.TIME_MORNING)
    is_done = models.BooleanField(_('Is done'), default=False, blank=True)
    is_public = models.BooleanField(_('Is public'), default=False, blank=True)
    is_shared = models.BooleanField(_('Is shared'), default=False, blank=True)
    is_new_comment = models.BooleanField(_('Is new comment'), default=False, blank=True)
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)
    sphere = models.ForeignKey(SelectedSphere,
                               on_delete=models.CASCADE,
                               related_name='goals',
                               verbose_name=_('Sphere'))
    user = models.ForeignKey(MainUser,
                             on_delete=models.CASCADE,
                             related_name='goals',
                             verbose_name=_('User'))

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')

    def __str__(self):
        return f'{self.id}: {self.name}'


class Observation(models.Model):
    observed = models.ForeignKey(MainUser,
                                 on_delete=models.CASCADE,
                                 related_name='observers',
                                 verbose_name=_('Observed'),
                                 null=True,
                                 blank=True)
    observer = models.ForeignKey(MainUser,
                                 on_delete=models.CASCADE,
                                 related_name='observed',
                                 verbose_name=_('Observer'))
    goal = models.OneToOneField(Goal, on_delete=models.CASCADE,
                                related_name='observation',
                                verbose_name=_('Goal'))
    is_confirmed = models.BooleanField(_('Is confirmed'), default=None, blank=True, null=True)

    class Meta:
        verbose_name = _('Observation')
        verbose_name_plural = _('Observations')

    def __str__(self):
        return f'{self.id}: {self.goal}'


class Comment(models.Model):
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)
    sender = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
        related_name='sender',
        null=True
    )
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        verbose_name=_('Goal'),
        related_name='messages'
    )
    text = models.TextField()
    is_owner = models.BooleanField(_('Owner'), null=True)
    is_read = models.BooleanField(_("Is read"), default=False, blank=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.id} {self.sender}'


class Visualization(models.Model):
    sphere = models.ForeignKey(SelectedSphere,
                             on_delete=models.CASCADE,
                             related_name='visualizations',
                             verbose_name=_('Sphere'))
    user = models.ForeignKey(MainUser,
                             on_delete=models.CASCADE,
                             related_name='visualizations',
                             verbose_name=_('User'))
    image = models.FileField(_('Image'),
                             upload_to=upload.visualization_document_path,
                             validators=[validators.validate_file_size, validators.basic_validate_images])
    annotation = models.TextField(_('Annotation'), null=True, blank=True)

    class Meta:
        verbose_name = _('Visualization')
        verbose_name_plural = _('Visualizations')

    def __str__(self):
        return f'{self.id}: {self.sphere}'

    def save(self, *args, **kwargs):
        if self.id is None:
            saved_image = self.image
            self.image = None
            super(Visualization, self).save(*args, **kwargs)
            self.image = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        # Вызов коструктора
        super(Visualization, self).save(*args, **kwargs)

        # Вытаскивается изображение
        image = Image.open(self.image.path)

        # Находим тэг изображения связаный с ориентацией
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        # Бывает при сохранении избражение поворачивется, тут ставим его назад
        if image._getexif():
            exif = dict(image._getexif().items())

            if exif.get(orientation) == 3:
                image = image.rotate(180, expand=True)
            elif exif.get(orientation) == 6:
                image = image.rotate(270, expand=True)
            elif exif.get(orientation) == 8:
                image = image.rotate(90, expand=True)

        # Сохраняем избражение и в параметр quality передаем значение качкества сжатия в процентах
        image.save(self.image.path, quality=20, optimize=True)


class UserAnswer(models.Model):
    question = models.CharField(_('Question'), max_length=500)
    user = models.ForeignKey(MainUser,
                             on_delete=models.CASCADE,
                             related_name='answers',
                             verbose_name=_('User'),
                             blank=True)
    answer = models.TextField(_('Answer'))
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def __str__(self):
        return f'{self.id}: {self.user}, {self.question}'


class Help(models.Model):
    user = models.ForeignKey(MainUser,
                             on_delete=models.CASCADE,
                             related_name='helps',
                             verbose_name=_('User'))
    text = models.TextField(_('Text'))
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)
    is_sent = models.BooleanField(_('Sent'), default=False, blank=True)

    class Meta:
        verbose_name = _('Help')
        verbose_name_plural = _('Help')

    def __str__(self):
        return f'{self.id}: {self.user}, {self.created_at}'


class UserResults(models.Model):
    user = models.ForeignKey(MainUser,
                             on_delete=models.CASCADE,
                             related_name='results',
                             verbose_name=_('User'),
                             blank=False, null=False)
    sphere_name = models.CharField(_('Sphere'), max_length=100, null=False, blank=False)
    number = models.IntegerField(_('Number of goals'), null=False, blank=False)

    class Meta:
        verbose_name = _('User results')

    def __str__(self):
        return f'{self.id}: {_("User")} - {self.user_id}'
