from rest_framework import serializers
from push_notifications.models import PeriodicNotification, NonCustomizableNotificationType


class PeriodicNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicNotification
        fields = '__all__'


class NonCustomizableNotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonCustomizableNotificationType
        fields = '__all__'
