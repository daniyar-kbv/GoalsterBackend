from django.contrib import admin
from main.models import Goal, Observation, Question, Help, SelectedSphere


class ObservationInline(admin.StackedInline):
    model = Observation
    extra = 0


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'time', 'is_done', 'is_shared')
    inlines = [ObservationInline]
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')


@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'created_at')
    search_fields = ['text', 'user']
    list_filter = ['created_at']
    autocomplete_fields = ['user']
