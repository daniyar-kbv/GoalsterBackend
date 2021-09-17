from django.urls import path
from users.views import UserViewSet, FeedViewSet, FeedV2ViewSet
from rest_framework import routers

urlpatterns = [
]

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('feed', FeedViewSet)
router.register('feed_v2', FeedV2ViewSet)

urlpatterns += router.urls