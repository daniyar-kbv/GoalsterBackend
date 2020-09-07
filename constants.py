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

MONTH = 1
YEAR = 2

TIME_FRAMES = (
    (MONTH, (_('Month'))),
    (YEAR, (_('Year')))
)

ACTIVATION_EMAIL_SUBJECT = 'test'
ACTIVATION_EMAIL_BODY_START = 'test'
ACTIVATION_EMAIL_BODY_END = 'test'

DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
DATE_FORMAT = '%d-%m-%Y'

MAX_REGULAR_FILE_SIZE = 10000000

IMAGE_EXTENSIONS = ['.jpg', '.png', '.jpeg']

FCM_SEND_URL = 'https://fcm.googleapis.com/fcm/send'

NOTIFICATION_3DAYS = 1
NOTIFICATION_BEFORE_END = 2
NOTIFICATION_END = 3

NOTIFICATION_TYPES = (
    (NOTIFICATION_3DAYS, '3 inactive days'),
    (NOTIFICATION_BEFORE_END, 'Before end of period'),
    (NOTIFICATION_END, 'End of period')
)

THREE_DAYS_TITLE = 'Ты 3 дня не заходил в приложение Goalster.'
THREE_DAYS_BODY = 'Кликни сюда и я покажу тебе то, для чего ты все начал.'
BEFORE_END_TITLE = 'Скоро подведение итогов!'
BEFORE_END_BODY = 'Ты готов?'
END_TITLE = '30 дневный период подходит к концу уже сегодня!'
END_BODY = 'Кликни сюда и подведи итоги.'

FIREBASE_SERVER_KEY = 'AAAAUR2qWDA:APA91bGLbMhQiCVFSBynt1R4nTtQ2dHeO1XSvfAnZTY_6Khh8xijVrLyWkIUAl_W96xTP1wcvy1TLScgX7pe3iaqlyNxEFQE5FG66I0FPNP-jai1b-IPPnccJOXCtGRM5FmJE7mBF_Yz'
