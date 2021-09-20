from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from users.models import ReactionType
from celebrities.models import Celebrity, CelebrityProfile, CelebritySphere, CelebrityReaction, CelebrityGoal
from utils import time, language
import constants


class CelebritySpheresFullSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CelebritySphere
        fields = ['id', 'name']

    def get_name(self, obj: CelebritySphere):
        return obj.get_name(language.get_request_language(self.context.get('request')))


class CelebrityProfileFeedSerialzier(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    specialization = serializers.SerializerMethodField()

    class Meta:
        model = CelebrityProfile
        fields = ['id', 'name', 'specialization', 'instagram_username', 'avatar']

    def get_name(self, obj: CelebrityProfile):
        return obj.get_name(language.get_request_language(self.context.get('request')))

    def get_specialization(self, obj: CelebrityProfile):
        return obj.get_specialization(language.get_request_language(self.context.get('request')))


class CelebrityFeedSerializer(serializers.ModelSerializer):
    profile = CelebrityProfileFeedSerialzier()
    selected = CelebritySpheresFullSerializer(many=True)
    reactions = serializers.SerializerMethodField()
    is_celebrity = serializers.SerializerMethodField()

    class Meta:
        model = Celebrity
        fields = ['id', 'profile', 'selected', 'reactions', 'is_celebrity']

    def get_reactions(self, obj):
        return map(
            lambda type:
            {
                'id': type.id,
                'emoji': type.emoji,
                'count': CelebrityReaction
                    .objects
                    .filter(user=obj,
                            type=type,
                            created_at__date=time.get_local_dt().date())
                    .count(),
                'reacted': CelebrityReaction
                .objects
                .filter(user=obj,
                            type=type,
                            created_at__date=time.get_local_dt().date(),
                            sender=self.context.get('request').user)
                .exists()
                if not isinstance(self.context.get('request').user, AnonymousUser)
                else None
            },
            ReactionType.objects.all()
        )

    def get_is_celebrity(self, obj):
        return True


class CelebrityProfileGoalsSerializer(serializers.ModelSerializer):
    sphere = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = CelebrityGoal
        fields = ('id', 'name', 'time', 'sphere')

    def get_name(self, obj: CelebrityGoal):
        return obj.get_name(language.get_request_language(self.context.get('request')))

    def get_sphere(self, obj):
        for index, sphere in enumerate(CelebritySphere.objects.filter(user=self.context.get('user'))):
            if sphere == obj.sphere:
                return index + 1
        return None


class CelebrityProfileFullSerializer(CelebrityFeedSerializer):
    goals = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta(CelebrityFeedSerializer.Meta):
        fields = CelebrityFeedSerializer.Meta.fields + ['goals', 'is_following']

    def get_goals(self, obj):
        queryset = CelebrityGoal.objects.filter(sphere__user=obj)
        morning_serializer = CelebrityProfileGoalsSerializer(
            queryset.filter(time=constants.TIME_MORNING).order_by('order'),
            many=True,
            context={
                'user': obj
            }
        )
        day_serializer = CelebrityProfileGoalsSerializer(
            queryset.filter(time=constants.TIME_DAY).order_by('order'),
            many=True,
            context={
                'user': obj
            }
        )
        evening_serializer = CelebrityProfileGoalsSerializer(
            queryset.filter(time=constants.TIME_EVENING).order_by('order'),
            many=True,
            context={
                'user': obj
            }
        )
        data = {
            'goals': len(morning_serializer.data) != 0 or len(day_serializer.data) != 0 or len(
                evening_serializer.data) != 0,
            'morning': morning_serializer.data,
            'day': day_serializer.data,
            'evening': evening_serializer.data
        }
        return data

    def get_is_following(self, obj):
        return obj.followers.filter(follower=self.context.get('request').user).exists()
