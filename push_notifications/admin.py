from django.contrib import admin
from django.db import models
from django.forms import TextInput
from push_notifications.models import NonCustomizableNotificationType, PeriodicNotification, DisposableNotification
import constants


@admin.register(NonCustomizableNotificationType)
class NonCustomizableNotificationTypeAdmin(admin.ModelAdmin):
    list_display = ['type']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})}
    }
    readonly_fields = ['type']

    def get_readonly_fields(self, request, obj: NonCustomizableNotificationType = None):
        if obj.type in [constants.NOTIFICATION_COMMENT, constants.NOTIFICATION_COMMENT_OBSERVER]:
            return self.readonly_fields + ['body_en', 'body_ru']
        return self.readonly_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PeriodicNotification)
class PeriodicNotificationAdmin(admin.ModelAdmin):
    list_display = ['title_en']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})}
    }


@admin.register(DisposableNotification)
class DisposableNotificationAdmin(admin.ModelAdmin):
    list_display = ['title_en']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})}
    }



