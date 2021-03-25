from django.contrib import admin
from main.models import Goal, Observation, Help, SelectedSphere, Comment


@admin.register(SelectedSphere)
class SelectedSphereAdmin(admin.ModelAdmin):
    search_fields = ['user__email']


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class ObservationInline(admin.StackedInline):
    model = Observation
    extra = 0
    fields = ['observer', 'is_confirmed']


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'date', 'time', 'is_done', 'is_shared')
    inlines = [ObservationInline, CommentInline]
    search_fields = ['name', 'user__email']
    autocomplete_fields = ['user', 'sphere']


@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'created_at')
    search_fields = ['text', 'user']
    list_filter = ['created_at', 'is_sent']
    autocomplete_fields = ['user']
