from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class NotificationEndpoint(ModelViewSet):
    queryset = Notification.objects.all().order_by('-id')
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        notifications = Notification.objects.filter(user=user)
        return notifications

    def perform_create(self, serializer):
        serializer.save()
