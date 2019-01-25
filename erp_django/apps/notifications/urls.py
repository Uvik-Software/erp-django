from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from .views import NotificationEndpoint

router = routers.DefaultRouter()
router.register(r'', NotificationEndpoint)

urlpatterns = [
    path('', include(router.urls))
]
