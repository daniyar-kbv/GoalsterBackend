from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from knowledge.models import Section, Story


class StoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Story
    extra = 0
    fields = ['title_en']
    readonly_fields = ['title_en']
    show_change_link = True


@admin.register(Section)
class SectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name_en', 'name_ru']
    inlines = [StoryInline]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    exclude = ['order']
    list_filter = ['section__name_en']