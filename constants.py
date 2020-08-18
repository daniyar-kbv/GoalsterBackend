from django.utils.translation import gettext_lazy as _

LANGUAGE_RUSSIAN = 1
LANGUAGE_ENGLISH = 2

LANGUAGES = (
    (LANGUAGE_ENGLISH, 'Русский'),
    (LANGUAGE_RUSSIAN, 'English'),
)

TIME_MORNING = 1
TIME_DAY = 2
TIME_EVENING = 3

TIME_TYPES = (
    (TIME_MORNING, _('Morning')),
    (TIME_DAY, _('Day')),
    (TIME_EVENING, _('Evening'))
)

ACTIVATION_EMAIL_SUBJECT = 'test'
ACTIVATION_EMAIL_BODY_START = 'test'
ACTIVATION_EMAIL_BODY_END = 'test'

DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
DATE_FORMAT = '%d-%m-%Y'

MAX_REGULAR_FILE_SIZE = 10000000

IMAGE_EXTENSIONS = ['.jpg', '.png', '.jpeg']
