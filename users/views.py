from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q, Count, Case, When
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from users.models import MainUser, Transaction, OTP, Reaction, Profile
from users.serializers import UserSendActivationEmailSerializer, UserShortSerializer, ChangeLanguageSerializer, \
    ChangeNotificationsSerializer, ConnectSerializer, TransactionSerializer, UserVerifyActivationEmailSerializer, \
    RegisterSerializer, VerifyOTPSerializer, ResendOTPSerializer, FeedSerializer, ReactSerializer, \
    ProfileFullSerializer, ProfileSerializer, UpdateProfileSerializer
from main.tasks import after_three_days, send_email
from main.models import SelectedSphere, Observation, UserResults
from main.serializers import UserResultsSerializer
from utils import encoding, response, permissions, emails, general, auth, time
import constants, datetime


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin):
    queryset = MainUser.objects.all()

    def get_serializer_class(self):
        return UserShortSerializer

    @action(detail=False, methods=['post'], name='send_activation_email')
    def send_activation_email(self, request, pk=None):
        return auth.send_verification_email(request, 1)

    @action(detail=False, methods=['post'], name='send_activation_email_v2')
    def send_activation_email_v2(self, request, pk=None):
        return auth.send_verification_email(request, 2)

    @action(detail=False, methods=['post'], name='send_activation_email_v3')
    def send_activation_email_v3(self, request, pk=None):
        return auth.send_verification_email(request, 3)

    @action(detail=False, methods=['post'], name='send_activation_email_v4')
    def send_activation_email_v4(self, request, pk=None):
        return auth.send_verification_email(request, 4)

    @action(detail=True, methods=['get'], name='verify-email')
    def verify_email(self, request, pk=None):
        try:
            email = encoding.decode(int(pk))
        except:
            return Response(response.make_messages([_('The used link is invalid')]), status.HTTP_400_BAD_REQUEST)
        try:
            user = MainUser.objects.get(email=email)
        except:
            user = MainUser.objects.create_user(email=email)
            user.save()
        return Response(auth.auth_user_data(user, request))

    @action(detail=False, methods=['post'], name='register')
    def register(self, request, pk=None):
        email = request.data.get('email')
        if email:
            context = {
                'request': request
            }
            try:
                user = MainUser.objects.get(email=email)
                if user.is_active:
                    return Response(response.make_messages([_("This email is already registered")]),
                                    status.HTTP_400_BAD_REQUEST)
                serializer = RegisterSerializer(instance=user, data=request.data, context=context)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except:
                serializer = RegisterSerializer(data=request.data, context=context)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                user.is_active = False
                user.save()
                return Response(serializer.data)
        return Response(response.make_messages([_("Enter a valid email address.")]), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='verify-otp')
    def verify_otp(self, request, pk=None):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = MainUser.objects.get(email=serializer.validated_data.get('email'))
            except:
                return Response(response.make_messages([_("User with such email doesn't exist")]),
                                status.HTTP_400_BAD_REQUEST)
            try:
                otp = OTP.objects.get(user=user, code=serializer.validated_data.get('otp'))
            except:
                return Response(response.make_messages([_('The code is invalid')]), status.HTTP_400_BAD_REQUEST)
            otp.delete_for_user(user)
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response(auth.auth_user_data(user, request))
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='login_resend_otp')
    def login_resend_otp(self, request, pk=None):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = MainUser.objects.get(email=serializer.validated_data.get('email'))
            except:
                return Response(response.make_messages([_("User with such email doesn't exist")]),
                                status.HTTP_404_NOT_FOUND)
            OTP.generate(user, request.headers.get('Accept-Language'))
            return Response(serializer.data)
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def temp_auth(self, request, pk=None):
        serializer = UserSendActivationEmailSerializer(data=request.data, context=request)
        if serializer.is_valid():
            try:
                user = MainUser.objects.get(email=serializer.validated_data.get('email'))
            except:
                user = MainUser.objects.create_user(email=serializer.validated_data.get('email'))
                user.save()
            return Response(auth.auth_user_data(user, request))
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], name='search', permission_classes=[permissions.IsAuthenticated])
    def search(self, request, pk=None):
        q = request.GET.get('q')
        users_data = []
        if q:
            users = MainUser.objects.filter(Q(email__icontains=q) & ~Q(email=request.user.email))
            serializer = UserShortSerializer(users, many=True)
            users_data = serializer.data
        return Response({
            "users": users_data
        })

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def connect(self, request, pk=None):
        user = request.user
        user.last_activity = timezone.now()
        user.received_three_days_notification = False
        after_three_days.apply_async(args=[user.id], eta=datetime.datetime.now() + datetime.timedelta(days=3))
        user.save()
        serializer = ConnectSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(auth.auth_user_data(user, request))

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def connect_v2(self, request, pk=None):
        user = request.user
        user.last_activity = timezone.now()
        user.save()
        serializer = ConnectSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(auth.auth_user_data(user, request))

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_language(self, request, pk=None):
        serializer = ChangeLanguageSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.language = serializer.validated_data.get('language')
            user.save()
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def notifications(self, request, pk=None):
        if request.method == 'GET':
            return Response({
                'enabled': request.user.notifications_enabled
            })
        elif request.method == 'POST':
            serializer = ChangeNotificationsSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                user.notifications_enabled = serializer.validated_data.get('enable')
                user.save()
                return Response()
            return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def results(self, request, pk=None):
        user = request.user
        results = UserResults.objects.filter(user=user)
        serializer = UserResultsSerializer(results, many=True)
        user.show_results = False
        user.save()
        return Response({
            'results': serializer.data
        })

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def premium(self, request, pk=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            files = []
            if request.headers.get('Accept-Language') == 'ru-ru':
                files.append('documents/visualization_board_ru.pdf')
                files.append('documents/to-do_list_ru.pdf')
                subject = constants.PREMIUM_EMAIL_SUBJECT_RU
            else:
                files.append('documents/visualization_board_en.pdf')
                files.append('documents/to-do_list_en.pdf')
                subject = constants.PREMIUM_EMAIL_SUBJECT_EN
            send_email.delay(subject,
                             emails.generate_premium_email(request.headers.get('Accept-Language')),
                             request.user.email,
                             files)
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def premium_v2(self, request, pk=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            if request.headers.get('Accept-Language') == 'ru-ru':
                subject = constants.PREMIUM_EMAIL_SUBJECT_RU
            else:
                subject = constants.PREMIUM_EMAIL_SUBJECT_EN
            send_email.delay(subject,
                             emails.generate_premium_email_v2(request.headers.get('Accept-Language')),
                             request.user.email,
                             html=True)
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request, pk=None):
        email = request.data.get('email')
        context = {
            'email': email
        }
        if Profile.objects.filter(user=request.user).exists():
            serializer = UpdateProfileSerializer(instance=request.user.profile, data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = UpdateProfileSerializer(data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
        payload = jwt_payload_handler(request.user)
        token = jwt_encode_handler(payload)
        return Response({
            'token': token,
            'profile': serializer.data,
            'email': email
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def following(self, request, pk=None):
        users = MainUser.objects.filter(followers=request.user)
        context = {
            'request': request
        }
        serializer = ProfileFullSerializer(users, many=True, context=context)
        return Response(serializer.data)


class FeedViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = MainUser.objects.filter(is_superuser=False, profile__isnull=False)
    permission_classes = [permissions.IsAuthenticated]

    def filter_queryset(self, queryset):
        if self.action == 'list':
            type = self.request.query_params.get('type', constants.FEED_TYPE_RECOMMENDATIONS)
            queryset = queryset.annotate(
                selected_count=Count('selected')
            ).filter(
                ~Q(id=self.request.user.id) &
                Q(selected_count__gt=0) &
                Q(in_recommendations=True)
            )
            queryset = queryset.annotate(
                goals_count=Count(
                    Case(When(Q(goals__date=time.get_local_dt().date()) & Q(goals__is_public=True), then=1))
                )
            ).filter(goals_count__gt=0)
            if type == constants.FEED_TYPE_RECOMMENDATIONS:
                queryset = queryset.order_by('-is_special', '-created_at')
                if not isinstance(self.request.user, AnonymousUser):
                    queryset = queryset.filter(~Q(followers=self.request.user))
            elif type == constants.FEED_TYPE_FOLLOWING:
                queryset = queryset.filter(followers=self.request.user)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProfileFullSerializer
        return FeedSerializer

    def get_permissions(self):
        if self.action == 'list' and \
                self.request.query_params.get('type', constants.FEED_TYPE_RECOMMENDATIONS) == constants.FEED_TYPE_RECOMMENDATIONS:
            return []
        return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        instance.followers.remove(user) \
        if instance.followers.filter(id=user.id).exists() else \
        instance.followers.add(user)
        context = {
            'request': request
        }
        serializer = ProfileFullSerializer(instance, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def react(self, request, pk=None):
        serializer = ReactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        try:
            reaction = Reaction.objects.get(type=serializer.reaction_type, user=user, sender=request.user)
            reaction.delete()
        except:
            reactions = Reaction.objects.filter(user=user, sender=request.user)
            reactions.delete()
            Reaction.objects.create(type=serializer.reaction_type, user=user, sender=request.user)
        return Response({
            'id': serializer.reaction_type.id,
            'emoji': serializer.reaction_type.emoji,
            'count': Reaction.objects.filter(user=user, type=serializer.reaction_type).count(),
            'reacted': Reaction.objects.filter(user=user, type=serializer.reaction_type, sender=request.user).exists()
        })