from django.utils.translation import gettext_lazy as _
import os

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

ACTIVATION_EMAIL_SUBJECT_EN = '24Goals Authorization'
ACTIVATION_EMAIL_BODY_START_EN = '''Hi!

I am Yerkezhan and I am the founder of 24Goals. Thank you for downloading my mobile app! I have created an account for you and it is almost ready. I just need you to verify your details by activating your account using the link below.'''
ACTIVATION_EMAIL_BODY_START_EN_V2 = '''Hi!

I am Yerkezhan and I am the founder of 24Goals. Thank you for downloading my mobile app! I have created an account for you and it is almost ready. I just need you to verify your details by activating your account using the code below.'''
ACTIVATION_EMAIL_BODY_END_EN = '''Follow us on Instagram: 24goalsapp

You can contact us at any time and leave a request. We value our clients and will not disregard your request.'''

ACTIVATION_EMAIL_SUBJECT_RU = '24Goals Авторизация'
ACTIVATION_EMAIL_BODY_START_RU = '''Привет!

Я Еркежан и я основатель 24Goals. Благодарю Вас за загрузку моего мобильного приложения!
Я создала для Вас аккаунт и он почти готов. Мне просто нужно, чтобы Вы подтвердили свои данные, активировав свою учетную запись, используя ссылку ниже. '''
ACTIVATION_EMAIL_BODY_START_RU_V2 = '''Привет!

Я Еркежан и я основатель 24Goals. Благодарю Вас за загрузку моего мобильного приложения!
Я создала для Вас аккаунт и он почти готов. Мне просто нужно, чтобы Вы подтвердили свои данные, активировав свою учетную запись, используя код ниже. '''
ACTIVATION_EMAIL_BODY_END_RU = '''Будь подписан на нас в Инстаграм - 24goalsapp 
Вы в любое время можете обратиться к нам. Мы ценим наших клиентов и не оставим без внимания Ваш запрос.'''

PREMIUM_EMAIL_SUBJECT_RU = 'Вы приобрели премиум'
PREMIUM_EMAIL_BODY_RU = '''- Уважаемый пользователь,

Это Еркежан. Поздравляю Вас с покупкой премиум версии в приложении 24Goals! Умное решение. 

В подарок к подписке я составила для вас советы по оформлению доски визуализации и чек-лист по эффективному мышлению. Файлы прикреплены к письму. 

Настройтесь на позитивные результаты и используйте приложение ежедневно.

Не забудьте подписаться на нас в Инстаграм, если вы еще этого не сделали - 24goalsapp 

Вы в любое время можете обратиться к нам. Мы ценим наших клиентов и не оставим без внимания Ваш запрос.'''

PREMIUM_EMAIL_SUBJECT_EN = 'Premium purchased'
PREMIUM_EMAIL_BODY_EN = '''- Dear user,

This is Yerkezhan. Congratulations on your purchase the premium version in the 24Goals app!  Smart decision.

As a present to your subscription, I made file with the tips for designing a visualization board and a to-do list for effective thinking. Files are attached to the letter. 

Tune in to positive results and use the app daily.

Don't forget to follow us on Instagram if you haven't already - 24goalsapp

You can contact us at any time.  We value our clients and will not disregard your request.'''

OBSERVATION_EMAIL_SUBJECT_RU = '24Goals Приглашение наблюдателя'
OBSERVATION_EMAIL_BODY_START_RU = '''- Уважаемый пользователь,

Это Еркежан. Вас выбрали в качестве наблюдателя в приложении 24Goals! 

Пожалуйста перейдите по ссылке ниже для подтверждения.'''
OBSERVATION_EMAIL_BODY_END_RU = '''Не забудьте подписаться на нас в Инстаграм, если вы еще этого не сделали - 24goalsapp 

Вы в любое время можете обратиться к нам. Мы ценим наших клиентов и не оставим без внимания Ваш запрос.'''

OBSERVATION_EMAIL_SUBJECT_EN = '24Goals Observer invitation'
OBSERVATION_EMAIL_BODY_START_EN = '''- Dear user,

This is Yerkezhan. You have been selected as an observer in the 24Goals app.

Please follow the link below to confirm.'''
OBSERVATION_EMAIL_BODY_END_EN = '''Don't forget to follow us on Instagram if you haven't already - 24goalsapp

You can contact us at any time.  We value our clients and will not disregard your request.'''

LINK_HINT_RU = '''* если ссылка не открывает приложение, зажмите ссылку, пока не появится лист действий,
а затем выберите опцию с надписью "Открыть в "24Goals""'''
LINK_HINT_EN = '''* if link doesn't open the app, long press the link until an action sheet comes up, 
then select the option that says "Open in "24Goals""'''

DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
DATE_FORMAT = '%d-%m-%Y'

MAX_REGULAR_FILE_SIZE = 10000000

IMAGE_EXTENSIONS = ['.jpg', '.png', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.gif', '.webp', '.tiff', '.tif', '.psd',
                    '.raw', '.arw', '.cr2', '.nrw', '.k25', '.bmp', '.dib', '.heif', '.heic', '.ind', '.indd', '.indt',
                    '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2']

FCM_SEND_URL = 'https://fcm.googleapis.com/fcm/send'

NOTIFICATION_3DAYS = 1
NOTIFICATION_BEFORE_END = 2
NOTIFICATION_END = 3

NOTIFICATION_TYPES = (
    (NOTIFICATION_3DAYS, '3 inactive days'),
    (NOTIFICATION_BEFORE_END, 'Before end of period'),
    (NOTIFICATION_END, 'End of period')
)

THREE_DAYS_TITLE_RU = 'Ты 3 дня не заходил в приложение 24Goals.'
THREE_DAYS_BODY_RU = 'Кликни сюда и я покажу тебе то, для чего ты все начал.'
BEFORE_END_TITLE_RU = 'Скоро подведение итогов!'
BEFORE_END_BODY_RU = 'Ты готов?'
END_TITLE_RU = '30 дневный период подходит к концу уже сегодня!'
END_BODY_RU = 'Кликни сюда и подведи итоги.'

THREE_DAYS_TITLE_EN = "You haven't opened the 24Goals app in 3 days."
THREE_DAYS_BODY_EN = "Click here and I'll show you what you started it all for."
BEFORE_END_TITLE_EN = 'Summing up soon!'
BEFORE_END_BODY_EN = 'Are you ready?'
END_TITLE_EN = 'The 30-day period is coming to an end today!'
END_BODY_EN = 'Click here and summarize.'

NEW_COMMENT_RU = 'Новый коментарий'
NEW_COMMENT_EN = 'New comment'

FIREBASE_SERVER_KEY = os.environ.get('FIREBASE_SERVER_KEY')

FIREBASE_DEEPLINKS_PREFIX = 'https://app.goalsterapp.com/'
FIREBASE_DEEPLINKS_LINK = 'https://goalsterapp.com'
FIREBASE_DEEPLINKS_ISI = '1532862482'
FIREBASE_DEEPLINKS_IBI = 'com.goalster.app'
FIREBASE_DEEPLINKS_DOMAIN = 'app.goalsterapp.com'

FIREBASE_DEEPLINKS_PREFIX_V4 = 'https://dynamic.24goalsapp.com/'
FIREBASE_DEEPLINKS_LINK_V4 = 'https://24goalsapp.com'
FIREBASE_DEEPLINKS_ISI_V4 = '1532862482'
FIREBASE_DEEPLINKS_IBI_V4 = 'com.goalster.app'
FIREBASE_DEEPLINKS_DOMAIN_V4 = 'dynamic.24goalsapp.com'

FIREBASE_SHORT_LINK_URL = f'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={os.environ.get("FIREBASE_API_KEY")}'

DEEPLINK_AUTH = 1
DEEPLINK_PREMIUM = 2

APPLE_TEST_EMAIL = 'jan.e.r.ebe.c.ca.lynn.tm.p@gmail.com'

HELP_RECIPIENT_EMAIL = 'feedback@24goalsapp.com'

PURCHASE_ONE_MONTH = 'com.goalsterapp.onemonth'
PURCHASE_THREE_MONTH = 'com.goalsterapp.threemonth'
PURCHASE_SIX_MONTH = 'com.goalsterapp.sixmonth'
PURCHASE_ONE_YEAR = 'com.goalsterapp.oneyear'

FIREBASE_TOPIC_INVITE = 'allUsers'

TOPIC_INVITE_TEXT_EN = 'Invite a friend or become an observer'
TOPIC_INVITE_TEXT_RU = 'Пригласи друга или стань наблюдателем'

FEED_TYPE_FOLLOWING = 'following'
FEED_TYPE_RECOMMENDATIONS = 'recommendations'