from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from PIL import Image, ExifTags
from utils import validators, upload, emails
import constants, random


class MainUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if not password:
            password = ''
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MainUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('Email'), unique=True)
    created_at = models.DateTimeField(_('Registration date'), auto_now_add=True, null=False, blank=True)
    language = models.PositiveSmallIntegerField(_('Language'), choices=constants.LANGUAGES,
                                                default=constants.LANGUAGE_RUSSIAN, blank=True)
    fcm_token = models.CharField(_('FCM Token'), max_length=500, null=True, blank=True)
    notifications_enabled = models.BooleanField(_('Notifications enabled'), default=True, blank=True)
    last_activity = models.DateTimeField(_('Last activity'), null=True, blank=True)
    received_three_days_notification = models.BooleanField(
        _('Received notification after 3 inactive days'),
        default=False,
        blank=True
    )

    is_premium = models.BooleanField(_('Premium'), default=False, blank=True)
    is_staff = models.BooleanField(_('Is admin'), default=False)
    is_active = models.BooleanField(_('Is active'), default=True)
    show_results = models.BooleanField(_('Show results'), default=False)
    in_recommendations = models.BooleanField(_('In recommendations'), default=True)
    is_special = models.BooleanField(_('Special'), default=False)

    objects = MainUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}: {self.email}'


class FollowModel(models.Model):
    user = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=_('User'),
    )
    follower = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Follower'),
    )

    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')

    def __str__(self):
        return f'({self.id}) {self.user.email} <- {self.follower.email}'


class Profile(models.Model):
    user = models.OneToOneField(
        MainUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )
    name = models.CharField(_('First name'), max_length=100)
    specialization = models.CharField(_('Specialization'), max_length=100)
    instagram_username = models.CharField(_('Instagram username'), max_length=100)
    avatar = models.FileField(
        _('Image'),
        upload_to=upload.avatar_document_path,
        validators=[validators.validate_file_size, validators.basic_validate_images]
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f'{self.id} {self.user}'

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete()
        except:
            pass

        if self.id is None:
            saved_image = self.avatar
            self.avatar = None
            super(Profile, self).save(*args, **kwargs)
            self.avatar = saved_image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Profile, self).save(*args, **kwargs)

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


class OTP(models.Model):
    user = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        related_name='otps',
        verbose_name=_('User')
    )
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, null=False, blank=True)
    code = models.CharField(_('Code'), max_length=4)

    def __str__(self):
        return f'{self.id} {self.user} {self.code}'

    @staticmethod
    def generate(user, language, request):
        from main.tasks import send_email
        code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        while OTP.objects.filter(code=code).exists():
            code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        otp = OTP.objects.create(user=user, code=code)
        if language == 'ru-ru':
            subject = constants.ACTIVATION_EMAIL_SUBJECT_RU
        else:
            subject = constants.ACTIVATION_EMAIL_SUBJECT_EN
        send_email.delay(
            subject,
            emails.generate_activation_email_v2(
                request,
                language,
                otp.code
            ),
            otp.user.email,
            html=True
        )

    @staticmethod
    def delete_for_user(user):
        otps = OTP.objects.filter(user=user)
        otps.delete()


class Transaction(models.Model):
    user = models.ForeignKey(MainUser,
                             on_delete=models.CASCADE,
                             related_name='transactions',
                             verbose_name=_('User'))
    identifier = models.CharField(_('Identifier'), max_length=1000)
    date = models.CharField(_('Date'), max_length=100)
    product_id = models.CharField(_('Product identifier'), max_length=500)
    time_amount = models.IntegerField(_('Time amount'))
    time_unit = models.PositiveSmallIntegerField(_('Time unit'), choices=constants.TIME_FRAMES, default=constants.MONTH)
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id}: {self.user} {self.product_id}'


class ReactionType(models.Model):
    emoji = models.CharField(_('Emoji'), max_length=100)

    class Meta:
        verbose_name = _('Reaction type')
        verbose_name_plural = _('Reaction types')

    def __str__(self):
        return f'{self.id} {self.emoji}'


class Reaction(models.Model):
    user = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='my_reactions'
    )
    sender = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
        related_name='sent_reactions'
    )
    type = models.ForeignKey(
        ReactionType,
        on_delete=models.PROTECT,
        verbose_name=_('Type'),
        related_name='reactions'
    )
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('Reaction')
        verbose_name_plural = _('Reactions')

    def __str__(self):
        return f'{self.id} {self.user} {self.type}'