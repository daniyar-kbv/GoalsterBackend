from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from knowledge.models import Section
from knowledge.serializers import SectionListSerializer, StoriesListSerializer


class SectionViewSet(GenericViewSet,
                     ListModelMixin):
    queryset = Section.objects.filter(is_active=True)
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return SectionListSerializer
        return SectionListSerializer

    @action(detail=True, methods=['get'])
    def stories(self, request, pk=None):
        stories = self.get_object().stories.all()
        serializer = StoriesListSerializer(stories, many=True, context=self.get_serializer_context())
        return Response(serializer.data)