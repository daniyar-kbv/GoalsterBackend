from rest_framework import routers
from knowledge.views import SectionViewSet

urlpatterns = [
]

router = routers.DefaultRouter()
router.register('sections', SectionViewSet)

urlpatterns += router.urls