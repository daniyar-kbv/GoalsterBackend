from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from main.models import Goal, Observation, Visualization, UserAnswer, SelectedSphere, Help
from main.serializers import ChooseSpheresSerializer, GoalListSerializer, GoalAddSerializer, AddEmotionSerializer, \
    UserAnswerListSerializer, VisualizationCreateSerializer, \
    VisualizationListSerializer, SelectedSphereSerializer, ObservedListSerializer, ObserversListSerializer, \
    ObservationAcceptSerializer, HelpCreateSerializer
from utils import permissions, response
import datetime, constants, PIL


class SphereViewSet(viewsets.GenericViewSet):
    queryset = SelectedSphere.objects.all()
    pagination_class = None

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def choose_spheres(self, request, pk=None):
        context = {
            'user': request.user
        }
        serializer = ChooseSpheresSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_spheres(self, request, pk=None):
        queryset = SelectedSphere.objects.filter(user=request.user)
        serializer = SelectedSphereSerializer(queryset, many=True)
        return Response(serializer.data)


class GoalViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin):
    queryset = Goal.objects.all()
    serializer_class = GoalListSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if request.GET.get('observation'):
            try:
                observation = Observation.objects.get(id=request.GET.get('observation'))
            except:
                return Response(response.make_messages([f'{_("Observation")} {_("does not exist")}']))
            if observation.observer != request.user:
                return Response(response.make_messages([_('You are not observer of this user')]))
            user = observation.observed
        queryset = Goal.objects.filter(user=user)
        if user != request.user:
            queryset = queryset.filter(observation__observer=request.user)
        date_str = request.GET.get('date')
        if date_str:
            date = datetime.datetime.strptime(date_str, constants.DATE_FORMAT).date()
        else:
            date = timezone.now().date()
        queryset = queryset.filter(date=date)
        context = {
            'user': request.user
        }
        morning_serializer = GoalListSerializer(queryset.filter(time=constants.TIME_MORNING).order_by('created_at'),
                                                 many=True, context=context)
        day_serializer = GoalListSerializer(queryset.filter(time=constants.TIME_DAY).order_by('created_at'),
                                                 many=True, context=context)
        evening_serializer = GoalListSerializer(queryset.filter(time=constants.TIME_EVENING).order_by('created_at'),
                                                 many=True, context=context)
        data = {
            'goals': len(morning_serializer.data) != 0 or len(day_serializer.data) != 0 or len(evening_serializer.data) != 0,
            'morning': morning_serializer.data,
            'day': day_serializer.data,
            'evening': evening_serializer.data
        }
        return Response(data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def calendar(self, request, pk=None):
        user = request.user
        if request.GET.get('observation'):
            try:
                observation = Observation.objects.get(id=request.GET.get('observation'))
            except:
                return Response(response.make_messages([f'{_("Observation")} {_("does not exist")}']))
            if observation.observer != request.user:
                return Response(response.make_messages([_('You are not observer of this user')]))
            user = observation.observed
        if SelectedSphere.objects.filter(user=user).count() != 3:
            return Response(response.make_messages([_('User had not selected spheres')]))
        start_date = SelectedSphere.objects.filter(user=user).first().created_at.date()
        end_date = SelectedSphere.objects.filter(user=user).first().expires_at.date()
        current_date = start_date
        data = []
        while current_date != end_date:
            data.append({
                'date': current_date.strftime(constants.DATE_FORMAT),
                'goals': {
                    'first': Goal.objects.filter(user=user,
                                                 sphere=SelectedSphere.objects.filter(user=user)[0],
                                                 date=current_date).count() != 0,
                    'second': Goal.objects.filter(user=user,
                                                 sphere=SelectedSphere.objects.filter(user=user)[1],
                                                 date=current_date).count() != 0,
                    'third': Goal.objects.filter(user=user,
                                                 sphere=SelectedSphere.objects.filter(user=user)[2],
                                                 date=current_date).count() != 0,
                }
            })
            current_date = current_date + datetime.timedelta(days=1)
        return Response({
            'items': data
        })


    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add(self, request, pk=None):
        context = {
            'user': request.user,
            'observer': request.data.pop('observer') if request.data.get('observer') else None,
            'request': request
        }
        serializer = GoalAddSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, permissions.OwnerPermission])
    def done(self, request, pk=None):
        try:
            goal = Goal.objects.get(id=pk)
        except:
            return Response(response.make_messages([f'{_("Goal")} {_("Does not exist")}']))
        goal.is_done = not goal.is_done
        goal.save()
        return Response()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def today(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        date = timezone.now().date()
        queryset = queryset.filter(date=date, user=request.user)
        context = {
            'user': request.user
        }
        print(queryset.filter(time=constants.TIME_DAY).order_by('created_at'))
        morning_serializer = GoalListSerializer(queryset.filter(time=constants.TIME_MORNING).order_by('created_at'),
                                                 many=True, context=context)
        day_serializer = GoalListSerializer(queryset.filter(time=constants.TIME_DAY).order_by('created_at'),
                                                 many=True, context=context)
        evening_serializer = GoalListSerializer(queryset.filter(time=constants.TIME_EVENING).order_by('created_at'),
                                                 many=True, context=context)
        data = {
            'total': {
                'first': Goal.objects.filter(user=request.user,
                                             sphere=SelectedSphere.objects.filter(user=request.user)[0],
                                             is_done=True).count(),
                'second': Goal.objects.filter(user=request.user,
                                              sphere=SelectedSphere.objects.filter(user=request.user)[1],
                                              is_done=True).count(),
                'third': Goal.objects.filter(user=request.user,
                                             sphere=SelectedSphere.objects.filter(user=request.user)[2],
                                             is_done=True).count()
            },
            'goals': {
                'goals': len(morning_serializer.data) != 0 or len(day_serializer.data) != 0 or len(evening_serializer.data) != 0,
                'morning': morning_serializer.data,
                'day': day_serializer.data,
                'evening': evening_serializer.data
            }
        }
        return Response(data)


class VisualizationViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    queryset = Visualization.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = []
        for sphere in SelectedSphere.objects.filter(user=request.user):
            visualizations = Visualization.objects.filter(user=request.user, sphere=sphere)
            serializer = VisualizationListSerializer(visualizations, many=True, context=request)
            data.append({
                'name': sphere.sphere,
                'visualizations': serializer.data
            })
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = VisualizationCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)


class EmotionsViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    queryset = UserAnswer.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserAnswerListSerializer

    def list(self, request, *args, **kwargs):
        queryset = UserAnswer.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'emotions': serializer.data
        })

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add(self, request, pk=None):
        context = {
            'user': request.user
        }
        serializer = AddEmotionSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)


class ObservationViewSet(viewsets.GenericViewSet,):
    queryset = Observation.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def observed(self, request, pk=None):
        queryset = Observation.objects.filter(observer=request.user, is_confirmed__in=[None, True]).distinct('observer')
        serializer = ObservedListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        try:
            observation = Observation.objects.get(id=pk)
        except:
            return Response(response.make_messages(f'{_("Observation")} {_("does not exist")}'))
        serializer = ObservationAcceptSerializer(data=request.data)
        if serializer.is_valid():
            for obs in Observation.objects.filter(observed=observation.observed, observer=request.user):
                obs.is_confirmed = serializer.validated_data.get('is_confirmed')
                obs.save()
            return Response()
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def observers(self, request, pk=None):
        queryset = Observation.objects.filter(observed=request.user, is_confirmed__in=[None, True]).distinct('observed')
        serializer = ObserversListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove(self, request, pk=None):
        try:
            observation = Observation.objects.get(id=pk)
        except:
            return Response(response.make_messages(f'{_("Observation")} {_("does not exist")}'))
        for obs in Observation.objects.filter(observed=request.user, observer=observation.observer):
            obs.is_confirmed = False
            obs.save()
        return Response()


class HelpViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    queryset = Help.objects.all()
    serializer_class = HelpCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)
