from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from users.models import MainUser, UserActivation, Transaction
from users.serializers import UserSendActivationEmailSerializer, UserShortSerializer, ChangeLanguageSerializer, \
    ChangeNotificationsSerializer, ConnectSerializer, TransactionSerializer, UserVerifyActivationEmailSerializer
from main.tasks import after_three_days, send_email
from main.models import SelectedSphere, Observation, UserResults
from main.serializers import UserResultsSerializer
from utils import encryption, response, permissions, emails, general
import constants, datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin):
    queryset = MainUser.objects.all()

    @action(detail=False, methods=['post'], name='send_activation_email')
    def send_activation_email(self, request, pk=None):
        serializer = UserSendActivationEmailSerializer(data=request.data)
        if serializer.is_valid():
            send_email.delay(constants.ACTIVATION_EMAIL_SUBJECT,
                             emails.generate_activation_email(serializer.validated_data.get('email')),
                             serializer.validated_data.get('email'))
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], name='verify-email')
    def verify_email(self, request, pk=None):
        email = encryption.decrypt(pk)
        try:
            user = MainUser.objects.get(email=email)
        except:
            user = MainUser.objects.create_user(email=email)
            user.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        spheres = []
        last_transaction = Transaction.objects.filter(user=user).first()
        premium_type = None
        if last_transaction:
            premium_type = f'{last_transaction.time_amount} ' \
                           f'{general.get_type_name(constants.TIME_FRAMES, last_transaction.time_unit)}' \
                           f'{_("s") if last_transaction.time_amount > 1 else ""}'
        for sphere in SelectedSphere.objects.filter(user=user):
            spheres.append({
                'id': sphere.id,
                'sphere': sphere.sphere,
                'description': sphere.description
            })
        data = {
            'token': token,
            'spheres': spheres,
            'email': user.email,
            'isPremium': user.is_premium,
            'premiumType': premium_type,
            'notConfirmedCount': Observation.objects.filter(Q(observer=user) & Q(is_confirmed=None)).distinct('observer').count()
        }
        return Response(data)

    # @action(detail=False, methods=['post'])
    # def temp_auth(self, request, pk=None):
    #     serializer = UserSendActivationEmailSerializer(data=request.data, context=request)
    #     if serializer.is_valid():
    #         try:
    #             user = MainUser.objects.get(email=serializer.validated_data.get('email'))
    #         except:
    #             user = MainUser.objects.create_user(email=serializer.validated_data.get('email'))
    #             user.save()
    #         payload = jwt_payload_handler(user)
    #         token = jwt_encode_handler(payload)
    #         spheres = []
    #         for sphere in SelectedSphere.objects.filter(user=user):
    #             spheres.append({
    #                 'id': sphere.id,
    #                 'sphere': sphere.sphere,
    #                 'description': sphere.description
    #             })
    #         data = {
    #             'token': token,
    #             'spheres': spheres
    #         }
    #         return Response(data)
    #     return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

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
        after_three_days.apply_async(args=[user.id], eta=datetime.datetime.now() + datetime.timedelta(days=3))
        user.save()
        serializer = ConnectSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        last_transaction = Transaction.objects.filter(user=user).first()
        premium_type = None
        if last_transaction:
            premium_type = f'{last_transaction.time_amount} ' \
                           f'{general.get_type_name(constants.TIME_FRAMES, last_transaction.time_unit)}' \
                           f'{_("s") if last_transaction.time_amount > 1 else ""}'
        spheres = []
        for sphere in SelectedSphere.objects.filter(user=user):
            spheres.append({
                'id': sphere.id,
                'sphere': sphere.sphere,
                'description': sphere.description
            })
        data = {
            'hasSpheres': SelectedSphere.objects.filter(user=request.user).count() == 3,
            'spheres': spheres,
            'email': user.email,
            'isPremium': user.is_premium,
            'premiumType': premium_type,
            'notConfirmedCount': Observation.objects.filter(Q(observer=request.user) & Q(is_confirmed=None)).distinct('observer').count()
        }
        return Response(data)

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
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)
