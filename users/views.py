from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from users.models import MainUser, Transaction
from users.serializers import UserSendActivationEmailSerializer, UserShortSerializer, ChangeLanguageSerializer, \
    ChangeNotificationsSerializer, ConnectSerializer, TransactionSerializer, UserVerifyActivationEmailSerializer
from main.tasks import after_three_days, send_email
from main.models import SelectedSphere, Observation, UserResults
from main.serializers import UserResultsSerializer
from utils import encoding, response, permissions, emails, general, auth
import constants, datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin):
    queryset = MainUser.objects.all()

    @action(detail=False, methods=['post'], name='send_activation_email')
    def send_activation_email(self, request, pk=None):
        return auth.send_verification_email(request, 1)

    @action(detail=False, methods=['post'], name='send_activation_email_v2')
    def send_activation_email_v2(self, request, pk=None):
        return auth.send_verification_email(request, 2)

    @action(detail=False, methods=['post'], name='send_activation_email_v3')
    def send_activation_email_v3(self, request, pk=None):
        return auth.send_verification_email(request, 3)

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
        results = UserResults.objects.filter(user=request.user)
        serializer = UserResultsSerializer(results, many=True)
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
