from django.contrib import admin
from django.forms import TextInput
from django.db import models
from adminsortable2.admin import SortableInlineAdminMixin
from celebrities.models import Celebrity, CelebrityProfile, CelebritySphere, CelebrityGoal


class CelebritySphereInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CelebritySphere
    min_num = 3
    max_num = 3
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '50'})}
    }
    show_change_link = True

    def has_delete_permission(self, request, obj=None):
        return False


class CelebrityProfileInline(admin.StackedInline):
    model = CelebrityProfile

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    exclude = ['order']
    model = Celebrity
    inlines = [CelebrityProfileInline, CelebritySphereInline]


class CelebrityGoalInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CelebrityGoal
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': TextInput(attrs={'size': '50'})}
    }


@admin.register(CelebritySphere)
class CelebritySphereAdmin(admin.ModelAdmin):
    inlines = [CelebrityGoalInline]
    readonly_fields = ['user']
    exclude = ['order']
    list_filter = ['user__profile__name_en']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
