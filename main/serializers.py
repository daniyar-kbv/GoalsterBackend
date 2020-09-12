from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from main.models import SelectedSphere, Goal, Observation, UserAnswer, Visualization, Help, UserResults
from users.models import MainUser
from utils import response
import constants


class SelectedSphereSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = SelectedSphere
        fields = ['id', 'name', 'description']

    def get_name(self, obj):
        return obj.sphere


class ChooseSpheresInnerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sphere = serializers.CharField()
    description = serializers.CharField()


class ChooseSpheresSerializer(serializers.Serializer):
    spheres = serializers.ListField(child=ChooseSpheresInnerSerializer())

    def create(self, validated_data):
        user = self.context.get('user')
        existing = SelectedSphere.objects.filter(user=user)
        existing.delete()
        selected = []
        for sphere in validated_data.get('spheres'):
            created = SelectedSphere.objects.create(description=sphere.get('description'),
                                                    sphere=sphere.get('sphere'),
                                                    user=user)
            selected.append({
                'id': created.id,
                'sphere': created.sphere,
                'description': created.description
            })

        return {
            'spheres': selected
        }


class UpdateSpheresSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedSphere
        fields = ['description']

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class GoalListSerializer(serializers.ModelSerializer):
    observer = serializers.SerializerMethodField()
    sphere = serializers.SerializerMethodField()
    is_confirmed = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = ('id', 'name', 'time', 'is_done', 'observer', 'is_confirmed','sphere')

    def get_observer(self, obj):
        try:
            observation = Observation.objects.get(goal=obj)
        except:
            return None
        return observation.observer.email

    def get_sphere(self, obj):
        for index, sphere in enumerate(SelectedSphere.objects.filter(user=self.context.get('user'))):
            if sphere == obj.sphere:
                return index + 1
        return None

    def get_is_confirmed(self, obj):
        try:
            observation = Observation.objects.get(goal=obj)
        except:
            return None
        return observation.is_confirmed


class GoalAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        goal = Goal.objects.create(**validated_data)
        if validated_data.get('is_shared'):
            user = self.context.get('user')
            if not user.is_premium:
                goal.delete()
                raise serializers.ValidationError(response.make_messages([_('You have to be premium to add observers')]))
            observer_id = self.context.get('observer')
            try:
                observer = MainUser.objects.get(id=observer_id)
            except:
                goal.delete()
                raise serializers.ValidationError(response.make_messages([f'{_("Observer")} {_("Does not exist")}']))
            observation = Observation.objects.create(observer=observer, goal=goal)
            observation._request = self.context.get('request')
            observation._created = True
            observation.save()
        return goal


class UserAnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['question', 'answer']


class UserAnswerAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'


class AddEmotionSerializer(serializers.Serializer):
    answers = serializers.ListField(child=UserAnswerAddSerializer())

    def validate_answers(self, value):
        if len(value) != 4:
            raise serializers.ValidationError(response.make_messages([_('Number of answers should be equal to 4')]))
        return value

    def create(self, validated_data):
        UserAnswer.objects.filter(user=self.context.get('user')).delete()
        answers = validated_data.get('answers')
        answer_objects = []
        for answer in answers:
            serializer = UserAnswerAddSerializer(data=answer)
            if serializer.is_valid():
                answer_objects.append(serializer.save(user=self.context.get('user')))
            else:
                for obj in answer_objects:
                    obj.delete()
                raise serializers.ValidationError(response.make_errors(serializer))
        return answer_objects


class VisualizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualization
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        if Visualization.objects.filter(sphere=validated_data.get('sphere'), user=self.context.get('user')).count() == 3:
            raise serializers.ValidationError(response.make_messages([_('You can not add more than 3 visualizations to one area')]))
        visualization = Visualization.objects.create(**validated_data)
        return visualization


class VisualizationListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Visualization
        fields = ['id', 'image', 'annotation']

    def get_image(self, obj):
        return self.context.build_absolute_uri(obj.image.url)


class SelectedSpheresObservedSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = SelectedSphere
        fields = ['sphere', 'count']

    def get_count(self, obj):
        return Goal.objects.filter(user=obj.user, is_done=True, sphere=obj).count()


class ObservedListSerializer(serializers.ModelSerializer):
    observed = serializers.SerializerMethodField()
    spheres = serializers.SerializerMethodField()

    class Meta:
        model = Observation
        fields = ['id', 'observed', 'is_confirmed', 'spheres']

    def get_observed(self, obj):
        return obj.observed.email

    def get_spheres(self, obj):
        string = ''
        spheres = SelectedSphere.objects.filter(user=obj.observed)
        for index, sphere in enumerate(spheres):
            count = Goal.objects.filter(user=obj.observed, is_done=True, sphere=sphere).count()
            string += f'{sphere.sphere} ({count})'
            if index != spheres.count() - 1:
                string += ', '
        return string


class ObserversListSerializer(serializers.ModelSerializer):
    observer = serializers.SerializerMethodField()

    class Meta:
        model = Observation
        fields = ['id', 'observer', 'is_confirmed']

    def get_observer(self, obj):
        return obj.observer.email


class ObservationAcceptSerializer(serializers.Serializer):
    is_confirmed = serializers.BooleanField()


class HelpCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'
        read_only_fields = ['user']


class UserResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResults
        fields = ['sphere_name', 'number']
