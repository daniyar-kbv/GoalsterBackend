from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from users.models import MainUser, UserActivation
from users.serializers import UserSendActivationEmailSerializer, UserShortSerializer, ChangeLanguageSerializer, \
    ChangeNotificationsSerializer, ConnectSerializer
from main.tasks import after_three_days
from main.models import SelectedSphere, Observation
from main.serializers import SelectedSphereSerializer
from utils import encryption, response, permissions
import constants, datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin):
    queryset = MainUser.objects.all()

    @action(detail=False, methods=['post'], name='send_activation_email')
    def send_activation_email(self, request, pk=None):
        serializer = UserSendActivationEmailSerializer(data=request.data, context=request)
        if serializer.is_valid():
            serializer.save()
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], name='verify-email')
    def verify_email(self, request, pk=None):
        email = encryption.decrypt(pk)
        activation = UserActivation.objects.filter(email=email).first()
        if not activation:
            return Response(response.make_messages([_('Activation is no longer valid')]), status.HTTP_400_BAD_REQUEST)
        if activation.is_active:
            activation.is_active = False
            user = MainUser.objects.create_user(email=activation.email)
            activation.user = user
            activation.save()
            user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            data = {
                'token': token
            }
            return Response(data)
        return Response(response.make_messages([_('Activation is no longer valid')]), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def temp_auth(self, request, pk=None):
        serializer = UserSendActivationEmailSerializer(data=request.data, context=request)
        if serializer.is_valid():
            try:
                user = MainUser.objects.get(email=serializer.validated_data.get('email'))
            except:
                user = MainUser.objects.create_user(email=serializer.validated_data.get('email'))
                user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            spheres = []
            for sphere in SelectedSphere.objects.filter(user=user):
                spheres.append({
                    'sphere': f'{sphere.id}',
                    'description': sphere.sphere
                })
            data = {
                'token': token,
                'spheres': spheres
            }
            return Response(data)
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
        after_three_days.apply_async(args=[user.id], eta=timezone.now() + datetime.timedelta(days=3))
        user.save()
        serializer = ConnectSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        data = {
            'hasSpheres': SelectedSphere.objects.filter(user=request.user).count() == 3,
            'email': user.email,
            'isPremium': user.is_premium,
            'notConfirmedCount': Observation.objects.filter(Q(observer=request.user) & Q(Q(is_confirmed=None) | Q(is_confirmed=True))).distinct('observer').count()
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

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def test_premium(self, request, pk=None):
        user = request.user
        user.is_premium = True
        user.save()
        return Response()
