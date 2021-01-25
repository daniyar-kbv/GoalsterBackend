from django.urls import path
from users.views import UserViewSet, FeedViewSet
from rest_framework import routers

urlpatterns = [
]

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('feed', FeedViewSet)

urlpatterns += router.urls