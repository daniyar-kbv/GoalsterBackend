from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from main.models import SelectedSphere, Goal, Observation, Comment
from users.models import MainUser, Transaction, Profile, OTP, ReactionType, Reaction
from utils import response
import constants


class UserSendActivationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()


class UserVerifyActivationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('id', 'email')
        read_only_fields = ['id']


class ChangeLanguageSerializer(serializers.Serializer):
    language = serializers.IntegerField()

    def validate_language(self, value):
        if value not in [1, 2]:
            raise serializers.ValidationError(response.make_messages([_('Language choices: 1, 2')]))
        return value


class ChangeNotificationsSerializer(serializers.Serializer):
    enable = serializers.BooleanField()


class ConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['fcm_token']

    def update(self, instance, validated_data):
        instance.fcm_token = validated_data.get('fcm_token', instance.fcm_token)
        instance.save()
        return instance


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user']


class UpdateProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.FileField(required=False)

    class Meta:
        model = Profile
        fields = ['name', 'specialization', 'instagram_username', 'avatar']

    def update(self, instance, validated_data):
        email = self.context.get('email')
        user = instance.user
        if email != user.email:
            user.email = email
            user.save()
        instance.name = validated_data.get('name', instance.name)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.instagram_username = validated_data.get('instagram_username', instance.instagram_username)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = MainUser
        fields = ['email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = MainUser.objects.create(**validated_data)
        Profile.objects.create(**profile_data, user=user)
        OTP.generate(user, self.context.get('request').headers.get('Accept-Language'))
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.get('profile')
        profile = instance.profile
        profile.name = profile_data.get('name', profile.name)
        profile.specialization = profile_data.get('specialization', profile.specialization)
        profile.instagram_username = profile_data.get('instagram_username', profile.instagram_username)
        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.save()
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        OTP.generate(instance, self.context.get('request').headers.get('Accept-Language'))
        return instance



class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ProfileFeedSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class SelectedSpheresFullSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = SelectedSphere
        fields = ['id', 'name', 'description', 'count']

    def get_name(self, obj):
        return obj.sphere

    def get_count(self, obj):
        return Goal.objects.filter(
            sphere=obj,
            is_done=True
        ).count()


class FollowingSerializer(serializers.ModelSerializer):
    profile = ProfileFeedSerialzier()

    class Meta:
        model = MainUser
        fields = ['id', 'email', 'profile', 'is_following']

    def get_is_following(self, obj):
        return obj.followers.filter(id=self.context.get('request').user.id).exists()


class FeedSerializer(serializers.ModelSerializer):
    profile = ProfileFeedSerialzier()
    selected = SelectedSpheresFullSerializer(many=True)
    reactions = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = MainUser
        fields = ['id', 'profile', 'selected', 'reactions']

    def get_reactions(self, obj):
        return map(
            lambda type:
            {
                'id': type.id,
                'emoji': type.emoji,
                'count': Reaction.objects.filter(user=obj, type=type).count(),
                'reacted': Reaction.objects.filter(user=obj, type=type, sender=self.context.get('request').user).exists()
            },
            ReactionType.objects.all()
        )


class ProfileGoalsSerializer(serializers.ModelSerializer):
    observer = serializers.SerializerMethodField()
    sphere = serializers.SerializerMethodField()
    is_confirmed = serializers.SerializerMethodField()
    new_comment = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = ('id', 'name', 'time', 'is_done', 'observer', 'is_confirmed', 'sphere', 'is_public', 'new_comment')

    def get_observer(self, obj):
        return None

    def get_sphere(self, obj):
        for index, sphere in enumerate(SelectedSphere.objects.filter(user=self.context.get('user'))):
            if sphere == obj.sphere:
                return index + 1
        return None

    def get_is_confirmed(self, obj):
        return None

    def get_new_comment(self, obj):
        return None


class ProfileFullSerializer(FeedSerializer):
    goals = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta(FeedSerializer.Meta):
        fields = FeedSerializer.Meta.fields + ['goals', 'is_following']

    def get_goals(self, obj):
        queryset = Goal.objects.filter(user=obj, is_public=True)
        morning_serializer = ProfileGoalsSerializer(
            queryset.filter(time=constants.TIME_MORNING).order_by('created_at'),
            many=True,
            context={
                'user': obj
            }
        )
        day_serializer = ProfileGoalsSerializer(
            queryset.filter(time=constants.TIME_DAY).order_by('created_at'),
            many=True,
            context={
                'user': obj
            }
        )
        evening_serializer = ProfileGoalsSerializer(
            queryset.filter(time=constants.TIME_EVENING).order_by('created_at'),
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
        return obj.followers.filter(id=self.context.get('request').user.id).exists()


class ReactSerializer(serializers.Serializer):
    reaction = serializers.IntegerField()

    def validate_reaction(self, value):
        if not ReactionType.objects.filter(id=value).exists():
            raise serializers.ValidationError(_('Does not exist'))
        return value

    @property
    def reaction_type(self):
        return ReactionType.objects.get(id=self.data.get('reaction'))