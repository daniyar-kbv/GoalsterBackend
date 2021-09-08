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
NOTIFICATION_COMMENT = 4
NOTIFICATION_COMMENT_OBSERVER = 5
NOTIFICATION_RATE = 6
NOTIFICATION_COMPLETE_GOALS = 7

THREE_DAYS_TITLE_RU = 'Ты 3 дня не заходил в приложение 24Goals.'
THREE_DAYS_BODY_RU = 'Кликни сюда и я покажу тебе то, для чего ты все начал.'
BEFORE_END_TITLE_RU = 'Скоро подведение итогов!'
BEFORE_END_BODY_RU = 'Ты готов?'
END_TITLE_RU = '30 дневный период подходит к концу уже сегодня!'
END_BODY_RU = 'Кликни сюда и подведи итоги.'
RATE_TITLE_RU = 'Оцени приложение'
RATE_BODY_RU = ''
COMPLETE_GOALS_TITLE_RU = 'Ты не завершил цели на сегодня'
COMPLETE_GOALS_BODY_RU = 'Вернись и заверши!'

THREE_DAYS_TITLE_EN = "You haven't opened the 24Goals app in 3 days."
THREE_DAYS_BODY_EN = "Click here and I'll show you what you started it all for."
BEFORE_END_TITLE_EN = 'Summing up soon!'
BEFORE_END_BODY_EN = 'Are you ready?'
END_TITLE_EN = 'The 30-day period is coming to an end today!'
END_BODY_EN = 'Click here and summarize.'
RATE_TITLE_EN = 'Rate our app'
RATE_BODY_EN = ''
COMPLETE_GOALS_TITLE_EN = 'You have not completed tour goals'
COMPLETE_GOALS_BODY_EN = 'Come back and complete!'

NEW_COMMENT_RU = 'Новый коментарий'
NEW_COMMENT_EN = 'New comment'
NEW_COMMENT_OBSERVER_RU = 'Ваш наставник оставил комментарий. Скорей заходи.'
NEW_COMMENT_OBSERVER_EN = 'Your mentor left a comment.'

NOTIFICATION_TYPES = (
    (NOTIFICATION_3DAYS, '3 inactive days'),
    (NOTIFICATION_BEFORE_END, 'Before end of period'),
    (NOTIFICATION_END, 'End of period'),
    (NOTIFICATION_COMMENT, 'New comment')
)

NON_CUSTOMIZABLE_NOTIFICATION_TYPES = (
    (NOTIFICATION_END, 'Об окончании периода'),
    (NOTIFICATION_BEFORE_END, 'За 3 дня до окончания периода'),
    (NOTIFICATION_COMMENT, 'Комментарий наставнику'),
    (NOTIFICATION_COMMENT_OBSERVER, 'Комментарий наблюдателю'),
    (NOTIFICATION_3DAYS, 'Если пользователь не заходит 3 дня'),
    (NOTIFICATION_RATE, 'Оцени приложение'),
    (NOTIFICATION_COMPLETE_GOALS, 'Для завершения целей')
)

NON_CUSTOMIZABLE_NOTIFICATION_TITLES_EN = (
    (NOTIFICATION_END, END_TITLE_EN),
    (NOTIFICATION_BEFORE_END, BEFORE_END_TITLE_EN),
    (NOTIFICATION_COMMENT, NEW_COMMENT_EN),
    (NOTIFICATION_COMMENT_OBSERVER, NEW_COMMENT_OBSERVER_EN),
    (NOTIFICATION_3DAYS, THREE_DAYS_TITLE_EN),
    (NOTIFICATION_RATE, RATE_TITLE_EN),
    (NOTIFICATION_COMPLETE_GOALS, COMPLETE_GOALS_TITLE_EN),
)

NON_CUSTOMIZABLE_NOTIFICATION_TITLES_RU = (
    (NOTIFICATION_END, END_TITLE_RU),
    (NOTIFICATION_BEFORE_END, BEFORE_END_TITLE_RU),
    (NOTIFICATION_COMMENT, NEW_COMMENT_RU),
    (NOTIFICATION_COMMENT_OBSERVER, NEW_COMMENT_OBSERVER_RU),
    (NOTIFICATION_3DAYS, THREE_DAYS_TITLE_RU),
    (NOTIFICATION_RATE, RATE_TITLE_RU),
    (NOTIFICATION_COMPLETE_GOALS, COMPLETE_GOALS_TITLE_RU),
)

NON_CUSTOMIZABLE_NOTIFICATION_BODIES_EN = (
    (NOTIFICATION_END, END_BODY_EN),
    (NOTIFICATION_BEFORE_END, BEFORE_END_BODY_EN),
    (NOTIFICATION_COMMENT, None),
    (NOTIFICATION_COMMENT_OBSERVER, None),
    (NOTIFICATION_3DAYS, THREE_DAYS_BODY_EN),
    (NOTIFICATION_RATE, RATE_BODY_EN),
    (NOTIFICATION_COMPLETE_GOALS, COMPLETE_GOALS_BODY_EN),
)

NON_CUSTOMIZABLE_NOTIFICATION_BODIES_RU = (
    (NOTIFICATION_END, END_BODY_RU),
    (NOTIFICATION_BEFORE_END, BEFORE_END_BODY_RU),
    (NOTIFICATION_COMMENT, None),
    (NOTIFICATION_COMMENT_OBSERVER, None),
    (NOTIFICATION_3DAYS, THREE_DAYS_BODY_RU),
    (NOTIFICATION_RATE, RATE_BODY_RU),
    (NOTIFICATION_COMPLETE_GOALS, COMPLETE_GOALS_BODY_RU),
)

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

EMAIL_TOP_EN = "Hi! I am Yerkezhan and I am the founder of 24Goals."
EMAIL_TOP_RU =  "Привет! Я Еркежан и я основатель 24Goals."

EMAIL_CODE_BODY_EN = "Thank you for downloading my mobile app!\nI have created an account for you and it is almost ready.\nI just need you to verify your details by\nactivating your account using the code below."
EMAIL_CODE_BODY_RU = "Благодарю тебя за загрузку моего приложения!\nЯ создала для тебя аккаунт и он почти готов.\nМне просто нужно, чтобы ты подтвердил свои данные,\nактивировав свою учетную запись, используя код ниже."

EMAIL_CODE_BODY_2_EN = "24Goals is a new social network where users\ncan plan, share their daily schedule,\ninspire and be inspired by others, set reactions,\nsubscribe, find like-minded people and a mentor,\nand develop networking through an internal messenger."
EMAIL_CODE_BODY_2_RU = "24Goals - это новая социальная сеть, в которой пользователи\nмогут планировать, делиться своим расписанием дня,\nвдохновлять и вдохновляться другими, ставить реакции,\nподписываться, находить единомышленников и наставника,\nразвивать нетворкинг путем внутренного мессенджера. "

EMAIL_BOTTOM_1_EN = "You can contact us at any time and leave a request.\nWe value our users and will not disregard your request."
EMAIL_BOTTOM_1_RU = "Ты в любое время можете обратиться к нам в разделе «помощь».\nМы ценим наших пользователей и не оставим без внимания твой запрос."

EMAIL_BOTTOM_2_EN = "Follow our useful community on Instagram:"
EMAIL_BOTTOM_2_RU = "Будь подписан на наш полезный комьюнити в Инстаграм -"

EMAIL_MENTOR_BODY_1_EN = "You have been selected as an mentor in the 24Goals app!"
EMAIL_MENTOR_BODY_1_RU = "Тебя выбрали в качестве наставника в приложении 24Goals!"

EMAIL_MENTOR_BODY_2_EN = "Go to the 24Goals app and go to the \"Profile\" tab.\nClick on the \"Observing\" tab and confirm yourself as a mentor.\nThank you very much!"
EMAIL_MENTOR_BODY_2_RU = "Зайди в приложение 24Goals и перейди во вкладку «Профиль».\nНажми на вкладку «Наблюдаю» и подтверди себя наставником.\nСпасибо тебе большое!"

EMAIL_PURCHASE_BODY_1_EN = "Congratulations on your purchase the premium version in the 24Goals app!"
EMAIL_PURCHASE_BODY_1_RU = "Поздравляю тебя с покупкой премиум версии в приложении 24Goals!"

EMAIL_PURCHASE_BODY_2_EN = "Smart decision."
EMAIL_PURCHASE_BODY_2_RU =  "Умное решение."

EMAIL_PURCHASE_BODY_3_EN = "As a gift to your subscription, I made file with the tips for\ndesigning a visualization board and a to-do list\nfor effective thinking."
EMAIL_PURCHASE_BODY_3_RU = "В подарок к подписке я составила для тебя советы по\nоформлению доски визуализации и чек-лист\nпо эффективному мышлению."

EMAIL_PURCHASE_BODY_4_EN = "Download from the link below.\nTune in to positive results and use the app daily."
EMAIL_PURCHASE_BODY_4_RU = "Настройся на позитивные результаты и используй\nприложение ежедневно."

EMAIL_PURCHASE_BODY_5_EN = "Link to download materials"
EMAIL_PURCHASE_BODY_5_RU = "Ссылка на скачивание материалов"

EMAIL_PURCHASE_LINK_EN = "https://drive.google.com/file/d/1376sapAOrObcBNwp_4iYcXjs6HXO0jX1/view?usp=sharing"
EMAIL_PURCHASE_LINK_RU = "https://drive.google.com/file/d/1xr5NJBsBXhhl6G4G9JjbKThSW5DyxFj2/view?usp=sharing"

WEEKDAY_MONDAY = 0
WEEKDAY_TUESDAY = 1
WEEKDAY_WEDNESDAY = 2
WEEKDAY_THURSDAY = 3
WEEKDAY_FRIDAY = 4
WEEKDAY_SATURDAY = 5
WEEKDAY_SUNDAY = 6

WEEKDAYS = [
    (WEEKDAY_MONDAY, 'Monday'),
    (WEEKDAY_TUESDAY, 'Tuesday'),
    (WEEKDAY_WEDNESDAY, 'Wednesday'),
    (WEEKDAY_THURSDAY, 'Thursday'),
    (WEEKDAY_FRIDAY, 'Friday'),
    (WEEKDAY_SATURDAY, 'Saturday'),
    (WEEKDAY_SUNDAY, 'Sunday'),
]

TOPIC_RU = '1'
TOPIC_EN = '2'

TOPICS = [
    (TOPIC_RU, 'RU'),
    (TOPIC_EN, 'EN')
]

LANGUAGES_TOPICS = [
    (LANGUAGE_RUSSIAN, TOPIC_RU),
    (LANGUAGE_ENGLISH, TOPIC_EN)
]