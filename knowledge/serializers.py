from rest_framework import serializers
from knowledge.models import Section, Story
from utils import language


class SectionListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'name', 'image']

    def get_name(self, obj: Section):
        return obj.get_name(language.get_request_language(self.context.get('request')))


class StoriesListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ['id', 'title', 'text', 'image', 'link']

    def get_title(self, obj: Story):
        return obj.get_title(language.get_request_language(self.context.get('request')))

    def get_text(self, obj: Story):
        return obj.get_text(language.get_request_language(self.context.get('request')))