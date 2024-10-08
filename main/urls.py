from django.urls import path
from main.views import SphereViewSet, GoalViewSet, EmotionsViewSet, VisualizationViewSet, \
    ObservationViewSet, HelpViewSet, CommentViewSet
from rest_framework import routers

urlpatterns = [
]

router = routers.DefaultRouter()
router.register('spheres', SphereViewSet)
router.register('goals', GoalViewSet)
router.register('emotions', EmotionsViewSet)
router.register('visualizations', VisualizationViewSet)
router.register('observations', ObservationViewSet)
router.register('help', HelpViewSet)
router.register('comments', CommentViewSet)

urlpatterns += router.urls