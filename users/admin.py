from django.contrib import admin
from users.models import MainUser, Transaction, Profile, OTP, ReactionType
from main.models import SelectedSphere, UserAnswer, Visualization, Goal, UserResults


class ProfileInline(admin.StackedInline):
    model = Profile


class OTPInline(admin.StackedInline):
    model = OTP
    extra = 0


class UserTransactionsInline(admin.StackedInline):
    model = Transaction
    extra = 0
    readonly_fields = ['user', 'identifier', 'date', 'product_id', 'time_amount', 'time_unit']


class UserResultsInline(admin.StackedInline):
    model = UserResults
    extra = 0


class SelectedSphereInline(admin.StackedInline):
    model = SelectedSphere
    extra = 0
    readonly_fields = ['expires_at']
    max_num = 3


class UserAnswerInline(admin.StackedInline):
    model = UserAnswer
    extra = 0
    max_num = 4


class VisualizationInline(admin.StackedInline):
    model = Visualization
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(VisualizationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'sphere':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(user=request._obj_)
            else:
                field.queryset = field.queryset.none()

        return field


@admin.register(MainUser)
class MainUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'is_staff', 'created_at')
    inlines = [ProfileInline, SelectedSphereInline, UserAnswerInline, VisualizationInline, UserResultsInline,
               UserTransactionsInline, OTPInline]
    readonly_fields = ['last_login', 'last_activity', 'received_three_days_notification']
    search_fields = ['email']
    list_filter = ['is_staff', 'is_active']
    ordering = ['-created_at']
    filter_horizontal = ['groups', 'user_permissions']

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(MainUserAdmin, self).get_form(request, obj, **kwargs)


@admin.register(ReactionType)
class ReactionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'emoji']