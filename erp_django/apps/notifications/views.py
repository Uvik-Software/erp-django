from django.forms import model_to_dict
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class NotificationEndpoint(ModelViewSet):
    queryset = Notification.objects.all().order_by('-id')
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        notifications = Notification.objects.filter(user=user).order_by('-id')
        return notifications

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            data = request.query_params.get('data', '')
            if data:
                Notification.objects.filter(user=request.user).delete()
            else:
                instance = self.get_object()
                self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        query = self.get_queryset()

        if not query:
            return Response(status=status.HTTP_204_NO_CONTENT)

        for instance in query:
            data = instance
            data.checked = True
            data = model_to_dict(data)

            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

        return Response(serializer.data)
