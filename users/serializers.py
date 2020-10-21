from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import MainUser, Transaction
from utils import response


class UserSendActivationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserVerifyActivationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


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


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user']
