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

ACTIVATION_EMAIL_SUBJECT_EN = 'GOALSTERS Authorization'
ACTIVATION_EMAIL_BODY_START_EN = '''Hi!

I am Yerkezhan and I am the founder of Goalsters. Thank you for downloading my mobile app! I have created an account for you and it is almost ready. I just need you to verify your details by activating your account using the link below.'''
ACTIVATION_EMAIL_BODY_END_EN = '''Follow us on Instagram: @goalsters

You can contact us at any time and leave a request. We value our clients and will not disregard your request.'''

ACTIVATION_EMAIL_SUBJECT_RU = 'GOALSTERS Авторизация'
ACTIVATION_EMAIL_BODY_START_RU = '''Привет!

Я Еркежан и я основатель Goalsters. Благодарю Вас за загрузку моего мобильного приложения!
Я создала для Вас аккаунт и он почти готов. Мне просто нужно, чтобы Вы подтвердили свои данные, активировав свою учетную запись, используя ссылку ниже. '''
ACTIVATION_EMAIL_BODY_END_RU = '''Будь подписан на нас в Инстаграм - @goalsters 
Вы в любое время можете обратиться к нам. Мы ценим наших клиентов и не оставим без внимания Ваш запрос.'''

PREMIUM_EMAIL_SUBJECT_RU = 'Вы приобрели премиум'
PREMIUM_EMAIL_BODY_RU = '''- Уважаемый пользователь,

Это Еркежан. Поздравляю Вас с покупкой премиум версии в приложении Goalsters! Умное решение. 

В подарок к подписке я составила для вас советы по оформлению доски визуализации и чек-лист по эффективному мышлению. Файлы прикреплены к письму. 

Настройтесь на позитивные результаты и используйте приложение ежедневно.

Не забудьте подписаться на нас в Инстаграм, если вы еще этого не сделали - @goalsters 

Вы в любое время можете обратиться к нам. Мы ценим наших клиентов и не оставим без внимания Ваш запрос.'''

PREMIUM_EMAIL_SUBJECT_EN = 'Premium purchased'
PREMIUM_EMAIL_BODY_EN = '''- Dear user,

This is Yerkezhan. Congratulations on your purchase the premium version in the Goalsters app!  Smart decision.

As a present to your subscription, I made file with the tips for designing a visualization board and a to-do list for effective thinking. Files are attached to the letter. 

Tune in to positive results and use the app daily.

Don't forget to follow us on Instagram if you haven't already - @goalsters

You can contact us at any time.  We value our clients and will not disregard your request.'''

OBSERVATION_EMAIL_SUBJECT_RU = 'GOALSTERS Приглашение наблюдателя'
OBSERVATION_EMAIL_BODY_START_RU = '''- Уважаемый пользователь,

Это Еркежан. Вас выбрали в качестве наблюдателя в приложении Goalsters! 

Пожалуйста перейдите по ссылке ниже для подтверждения.'''
OBSERVATION_EMAIL_BODY_END_RU = '''Не забудьте подписаться на нас в Инстаграм, если вы еще этого не сделали - @goalsters 

Вы в любое время можете обратиться к нам. Мы ценим наших клиентов и не оставим без внимания Ваш запрос.'''

OBSERVATION_EMAIL_SUBJECT_EN = 'GOALSTERS Observer invitation'
OBSERVATION_EMAIL_BODY_START_EN = '''- Dear user,

This is Yerkezhan. You have been selected as an observer in the Goalsters app.

Please follow the link below to confirm.'''
OBSERVATION_EMAIL_BODY_END_EN = '''Don't forget to follow us on Instagram if you haven't already - @goalsters

You can contact us at any time.  We value our clients and will not disregard your request.'''

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

THREE_DAYS_TITLE_RU = 'Ты 3 дня не заходил в приложение Goalsters.'
THREE_DAYS_BODY_RU = 'Кликни сюда и я покажу тебе то, для чего ты все начал.'
BEFORE_END_TITLE_RU = 'Скоро подведение итогов!'
BEFORE_END_BODY_RU = 'Ты готов?'
END_TITLE_RU = '30 дневный период подходит к концу уже сегодня!'
END_BODY_RU = 'Кликни сюда и подведи итоги.'

THREE_DAYS_TITLE_EN = "You haven't opened the Goalsters app in 3 days."
THREE_DAYS_BODY_EN = "Click here and I'll show you what you started it all for."
BEFORE_END_TITLE_EN = 'Summing up soon!'
BEFORE_END_BODY_EN = 'Are you ready?'
END_TITLE_EN = 'The 30-day period is coming to an end today!'
END_BODY_EN = 'Click here and summarize.'

FIREBASE_SERVER_KEY = 'AAAAUR2qWDA:APA91bGLbMhQiCVFSBynt1R4nTtQ2dHeO1XSvfAnZTY_6Khh8xijVrLyWkIUAl_W96xTP1wcvy1TLScgX7pe3iaqlyNxEFQE5FG66I0FPNP-jai1b-IPPnccJOXCtGRM5FmJE7mBF_Yz'

FIREBASE_DEEPLINKS_PREFIX = 'https://app.goalsterapp.com/'
FIREBASE_DEEPLINKS_LINK = 'https://goalsterapp.com'
FIREBASE_DEEPLINKS_ISI = '1532862482'
FIREBASE_DEEPLINKS_IBI = 'com.goalster.app'
FIREBASE_DEEPLINKS_EFR = '1'

DEEPLINK_AUTH = 1
DEEPLINK_PREMIUM = 2

APPLE_TEST_EMAIL = 'jan.e.r.ebe.c.ca.lynn.tm.p@gmail.com'