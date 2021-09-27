from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from knowledge.models import Section, Story


class StoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Story
    extra = 0
    fields = ['text_en']
    readonly_fields = ['text_en']
    show_change_link = True


@admin.register(Section)
class SectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name_en', 'name_ru', 'is_active']
    list_filter = ['is_active']
    inlines = [StoryInline]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['text_en', 'is_active']
    exclude = ['order']
    list_filter = ['section__name_en', 'is_active']