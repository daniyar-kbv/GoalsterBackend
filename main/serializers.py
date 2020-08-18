from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from main.models import SelectedSphere, Goal, Observation, Question, UserAnswer, Visualization, Help
from users.models import MainUser
from utils import response
import constants


class SelectedSphereSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = SelectedSphere
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.sphere


class ChooseSpheresInnerSerializer(serializers.Serializer):
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
                'sphere': created.id,
                'description': created.sphere
            })
        return {
            'spheres': selected
        }


class GoalListSerializer(serializers.ModelSerializer):
    observer = serializers.SerializerMethodField()
    sphere = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = ('id', 'name', 'time', 'is_done', 'observer', 'sphere')

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
            observation = Observation.objects.create(observed=user, observer=observer, goal=goal)
            observation._request = self.context.get('request')
            observation._created = True
            observation.save()
        return goal


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'name', 'placeholder')


class UserAnswerListSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'answer']

    def get_question(self, obj):
        return obj.question.name


class UserAnswerAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
        read_only_fields = ['question']


class AddEmotionSerializer(serializers.Serializer):
    answers = serializers.ListField(child=serializers.CharField())

    def validate_answers(self, value):
        if len(value) != Question.objects.count():
            raise serializers.ValidationError(response.make_messages([_('Number of answers should be equal to 4')]))
        return value

    def create(self, validated_data):
        UserAnswer.objects.all().delete()
        for index, answer in enumerate(validated_data.get('answers')):
            data = {
                'answer': answer
            }
            serializer = UserAnswerAddSerializer(data=data)
            try:
                question = Question.objects.get(position=index + 1)
            except:
                raise serializers.ValidationError(response.make_messages([f"{_('Question')} {_('Does not exist')}"]))
            if serializer.is_valid():
                serializer.save(user=self.context.get('user'), question=question)
            else:
                raise serializers.ValidationError(response.make_errors(serializer))
        return validated_data.get('answers')


class VisualizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualization
        fields = '__all__'
        read_only_fields = ['user']


class VisualizationListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Visualization
        fields = ['id', 'image', 'annotation']

    def get_image(self, obj):
        return self.context.build_absolute_uri(obj.image.url)


class ObservedListSerializer(serializers.ModelSerializer):
    observed = serializers.SerializerMethodField()

    class Meta:
        model = Observation
        fields = ['id', 'observed', 'is_confirmed']

    def get_observed(self, obj):
        return obj.observed.email


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