from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, get_confirmation_code


app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

auth_patterns = [
    path('login/', get_confirmation_code, name='get_confirmation_code'),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
]
