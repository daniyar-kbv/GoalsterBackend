from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import constants


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
    notifications_enabled = models.BooleanField(_('Notifications enabled'), default=False, blank=True)
    last_activity = models.DateTimeField(_('Last activity'), null=True, blank=True)

    is_premium = models.BooleanField(_('Premium'), default=False, blank=True)
    is_staff = models.BooleanField(_('Is admin'), default=False)
    is_active = models.BooleanField(_('Is active'), default=True)

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


class UserActivation(models.Model):
    email = models.EmailField(_('Email'))
    is_active = models.BooleanField(_('Is active'), default=True, blank=True)
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True, blank=True)
    user = models.OneToOneField(MainUser,
                                on_delete=models.CASCADE,
                                related_name='activation',
                                verbose_name=_('User'),
                                blank=True, null=True)

    class Meta:
        verbose_name = _('User activation')
        verbose_name_plural = _('User activations')

    def __str__(self):
        return f'{self.id}: {self.email}'


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

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return f'{self.id}: {self.user} {self.product_id}'
