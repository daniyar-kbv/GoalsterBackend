from django.core.files import File
from faker import Faker
from users.models import MainUser, Profile
from main.models import SelectedSphere, Goal
from utils.decorators import singleton

import random
import constants
import datetime as dt

fake = Faker(locale='ru_RU')

@singleton
class TestGenerator:
    def create_test_data(self, number):
        for i in range(0, 50):
            user = self.__create_user()
            self.__create_profile(user)
            spheres = self.__create_spheres(user)
            self.__create_goals(user, spheres)

    def __create_user(self) -> MainUser:
        return MainUser.objects.create(
            email=fake.email(),
            language=random.choice(constants.LANGUAGES)[0],
            is_premium=bool(random.getrandbits(1)),
            in_recommendations=True,
            is_special=bool(random.getrandbits(1))
        )

    def __create_profile(self, user: MainUser) -> Profile:
        avatar_file = open(f'/test_images/avatars/{random.randint(1, 12)}.jpg')
        avatar = File(avatar_file)

        profile = Profile.objects.create(
            user=user,
            avatar=avatar,
            name=fake.first_name(),
            specialization=fake.job(),
            instagram_username=fake.email(),
        )

        avatar_file.close()
        return profile

    def __create_sphere(self, user: MainUser):
        return SelectedSphere.objects.create(
            description=fake.sentence(),
            sphere=fake.word(),
            user=user
        )

    def __create_spheres(self, user: MainUser) -> [SelectedSphere]:
        return list(map(lambda i: self.__create_sphere(user), [i for i in range(0, 3)]))

    def __create_goals(self, user: MainUser, spheres: [SelectedSphere]):
        start_date = dt.date.today()
        day_count = 10
        for single_date in (start_date + dt.timedelta(n) for n in range(day_count)):
            for i in range(0, 6):
                Goal.objects.create(
                    name=fake.sentence(),
                    date=single_date,
                    time=random.choice(constants.TIME_TYPES)[0],
                    is_done=bool(random.getrandbits(1)),
                    is_public=True,
                    is_shared=False,
                    is_new_comment=False,
                    sphere=random.choice(spheres),
                    user=user
                )