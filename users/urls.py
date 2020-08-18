from django.urls import path
from users.views import UserViewSet
from rest_framework import routers

urlpatterns = [
]

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns += router.urls