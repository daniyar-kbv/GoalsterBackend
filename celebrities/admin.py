from django.contrib import admin
from nested_inline.admin import NestedTabularInline, NestedStackedInline, NestedModelAdmin
from celebrities.models import Celebrity, CelebrityProfile, CelebritySphere, CelebrityGoal


class CelebrityGoalInline(NestedTabularInline):
    model = CelebrityGoal
    extra = 0


class CelebritySphereInline(NestedTabularInline):
    model = CelebritySphere
    min_num = 3
    max_num = 3
    inlines = [CelebrityGoalInline]


class CelebrityProfileInline(NestedStackedInline):
    model = CelebrityProfile


@admin.register(Celebrity)
class CelebrityAdmin(NestedModelAdmin):
    model = Celebrity
    inlines = [CelebrityProfileInline, CelebritySphereInline]
