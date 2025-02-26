from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from apps.chat.api.serializers import ChatMessageSerializer, FileSerializer
from apps.chat.models import ChatMessage, ChatFile


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    Class representing a chat messages viewset
    """

    serializer_class = ChatMessageSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["date"]
    filterset_fields = [
        "user__username",
        "date",
        "room__id",
    ]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        return ChatMessage.objects.filter(room_id__in=[self.request.GET.get("room")])


class FileViewSet(viewsets.ModelViewSet):
    """
    Class representing a chat media viewset
    """

    serializer_class = FileSerializer
    http_method_names = ["get", "head", "options", "post"]
    queryset = ChatFile.objects.all()
