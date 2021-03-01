from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from main.models import Goal, Observation, Visualization, UserAnswer, SelectedSphere, Help, Comment
from main.serializers import ChooseSpheresSerializer, GoalListSerializer, GoalAddSerializer, AddEmotionSerializer, \
    UserAnswerListSerializer, VisualizationCreateSerializer, \
    VisualizationListSerializer, SelectedSphereSerializer, ObservedListSerializer, ObserversListSerializer, \
    ObservationAcceptSerializer, HelpCreateSerializer, UpdateSpheresSerializer, CommentCreateSerializer, \
    CommentListSerializer
from main.tasks import send_email
from utils import permissions, response, deeplinks, encoding, time, general
import datetime, constants, PIL, requests


class SphereViewSet(viewsets.GenericViewSet,
                    mixins.UpdateModelMixin):
    queryset = SelectedSphere.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'update':
            return UpdateSpheresSerializer
        return UpdateSpheresSerializer

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

    @action(detail=False, methods=['get', 'put'], permission_classes=[permissions.IsAuthenticated])
    def my_spheres(self, request, pk=None):
        if request.method == 'GET':
            queryset = SelectedSphere.objects.filter(user=request.user)
            serializer = SelectedSphereSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.method == 'PUT':
            new_descriptions = request.data.get('descriptions')
            serializers = []
            for index, sphere in enumerate(SelectedSphere.objects.filter(user=request.user)):
                serializer = UpdateSpheresSerializer(instance=sphere, data={
                    'description': new_descriptions[index]
                })
                if not serializer.is_valid():
                    return Response(response.make_errors(serializer))
                serializers.append(serializer)
            serializer_data = []
            for serializer in serializers:
                sphere = serializer.save()
                serializer_data.append({
                    'id': sphere.id,
                    'sphere': sphere.sphere,
                    'description': sphere.description
                })
            return Response(data={
                'spheres': serializer_data
            })

    @action(detail=False, methods=['get'])
    def test(self, request, pk=None):
        print('/'.join(request.build_absolute_uri().split('/')[0:3]))
        return Response()


class GoalViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin):
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
            date = time.get_local_dt().date()
        queryset = queryset.filter(date=date)
        context = {
            'user': user
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

    def update(self, request, *args, **kwargs):
        goal = self.get_object()
        context = {
            'user': request.user,
            'observer': request.data.pop('observer') if request.data.get('observer') else None,
            'request': request
        }
        serializer = GoalAddSerializer(instance=goal, data=request.data, context=context)
        if serializer.is_valid():
            goal = self.perform_update(serializer)
            out_serializer = GoalListSerializer(goal)
            return Response(out_serializer.data)
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

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
        return general.add_goal(response)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_v2(self, request, pk=None):
        return general.add_goal(request)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_v3(self, request, pk=None):
        return general.add_goal(request)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_v4(self, request, pk=None):
        return general.add_goal(request)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_v5(self, request, pk=None):
        return general.add_goal(request)

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
        date = time.get_local_dt().date()
        queryset = queryset.filter(date=date, user=request.user)
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


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    pagination_class = None

    def filter_queryset(self, queryset):
        if self.action == 'list':
            queryset = queryset.filter(goal_id=self.request.query_params.get('goal'))
            try:
                goal = Goal.objects.get(id=self.request.query_params.get('goal'))
            except:
                return queryset
            for comment in queryset.filter(is_owner=goal.user != self.request.user):
                comment.is_read = True
                comment.save()
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        elif self.action == 'list':
            try:
                goal = Goal.objects.get(id=self.request.query_params.get('goal'))
                goal.is_new_comment = False
                goal.save()
            except:
                pass
            return CommentListSerializer
        return CommentListSerializer


class VisualizationViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin):
    queryset = Visualization.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = []
        for sphere in SelectedSphere.objects.filter(user=request.user):
            visualizations = Visualization.objects.filter(user=request.user, sphere=sphere)
            serializer = VisualizationListSerializer(visualizations, many=True, context=request)
            data.append({
                'id': sphere.id,
                'name': sphere.sphere,
                'visualizations': serializer.data
            })
        return Response({
            'spheres': data
        })

    def create(self, request, *args, **kwargs):
        context = {
            'user': request.user
        }
        serializer = VisualizationCreateSerializer(data=request.data, context=context)
        if serializer.is_valid():
            visualization = serializer.save(user=request.user)
            out_serializer = VisualizationListSerializer([visualization], many=True, context=request)
            data = {
                'id': visualization.sphere.id,
                'name': visualization.sphere.sphere,
                'visualizations': out_serializer.data
            }
            return Response(data)
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response()


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
            return self.list(request)
        return Response(response.make_errors(serializer), status.HTTP_400_BAD_REQUEST)


class ObservationViewSet(viewsets.GenericViewSet,):
    queryset = Observation.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def observed(self, request, pk=None):
        queryset = Observation.objects.filter(Q(observer=request.user) & Q(Q(is_confirmed=None) | Q(is_confirmed=True))).distinct('observer')
        serializer = ObservedListSerializer(queryset, many=True)
        return Response({
            'observed': serializer.data
        })

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
        queryset = Observation.objects.filter(Q(observed=request.user) & Q(Q(is_confirmed=None) | Q(is_confirmed=True))).distinct('observer')
        serializer = ObserversListSerializer(queryset, many=True)
        return Response({
            'observers': serializer.data
        })

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
