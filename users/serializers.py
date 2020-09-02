from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import UserActivation, MainUser
from utils import response


class UserSendActivationEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivation
        fields = '__all__'

    def create(self, validated_data):
        try:
            activation = UserActivation.objects.get(email=validated_data.get('email'))
        except:
            activation = UserActivation.objects.create(**validated_data)
        activation._request = self.context
        activation._created = True
        activation.save()
        return activation


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('id', 'email')


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
