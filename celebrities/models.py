from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image, ExifTags
from users.models import MainUser, ReactionType
from utils import upload, validators
import constants


class Celebrity(models.Model):
    is_active = models.BooleanField(_('Is active'), default=False)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Celebrity')
        verbose_name_plural = _('Celebrities')

    def __str__(self):
        return f'Celebrity ({self.id}): {self.profile.name}'


class CelebrityProfile(models.Model):
    user = models.OneToOneField(
        Celebrity,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )

    name = models.CharField(_('First name'), max_length=100)
    specialization = models.CharField(_('Specialization'), max_length=100)
    instagram_username = models.CharField(_('Instagram username'), max_length=100)
    avatar = models.FileField(
        _('Image'),
        upload_to=upload.celebrity_avatar_document_path,
        validators=[validators.validate_file_size, validators.basic_validate_images]
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f'{self.id} {self.user}'

    def save(self, *args, **kwargs):
        try:
            this = CelebrityProfile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete()
        except:
            pass

        if self.id is None:
            saved_image = self.avatar
            self.avatar = None
            super(CelebrityProfile, self).save(*args, **kwargs)
            self.avatar = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(CelebrityProfile, self).save(*args, **kwargs)

        image = Image.open(self.avatar.path)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        if image._getexif():
            exif = dict(image._getexif().items())

            if exif.get(orientation) == 3:
                image = image.rotate(180, expand=True)
            elif exif.get(orientation) == 6:
                image = image.rotate(270, expand=True)
            elif exif.get(orientation) == 8:
                image = image.rotate(90, expand=True)

        image.save(self.avatar.path, quality=20, optimize=True)


class CelebrityFollowModel(models.Model):
    user = models.ForeignKey(
        Celebrity,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=_('User'),
    )
    follower = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        related_name='following_celebrities',
        verbose_name=_('Follower'),
    )

    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')

    def __str__(self):
        return f'({self.id}) {self.user.name} <- {self.follower.email}'


class CelebrityReaction(models.Model):
    user = models.ForeignKey(
        Celebrity,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='my_reactions'
    )
    sender = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
        related_name='sent_celebrity_reactions'
    )
    type = models.ForeignKey(
        ReactionType,
        on_delete=models.PROTECT,
        verbose_name=_('Type'),
        related_name='celebrity_reactions'
    )
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('Reaction')
        verbose_name_plural = _('Reactions')

    def __str__(self):
        return f'{self.id} {self.user} {self.type}'


class CelebritySphere(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    user = models.ForeignKey(
        Celebrity,
        on_delete=models.CASCADE,
        related_name='selected',
        verbose_name=_('User')
    )

    class Meta:
        verbose_name = _('Selected sphere')
        verbose_name_plural = _('Selected spheres')

    def __str__(self):
        return f'{self.id}: {self.user}, {self.name}'


class CelebrityGoal(models.Model):
    sphere = models.ForeignKey(CelebritySphere,
                               on_delete=models.CASCADE,
                               related_name='goals',
                               verbose_name=_('Sphere'))

    name = models.TextField(_('Name'))
    time = models.PositiveSmallIntegerField(_('Time of the day'),
                                            choices=constants.TIME_TYPES,
                                            default=constants.TIME_MORNING)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')

    def __str__(self):
        return f'{self.id}: {self.name}'