from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.response import Response

from apps.chat.api.serializers import ChatMessageSerializer, FileSerializer, ChatRoomSerializer
from apps.chat.models import ChatMessage, ChatFile, ChatRoom


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


class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    http_method_names = ["get", "head", "options", "post"]

    def get_queryset(self):
        return ChatRoom.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        room = ChatRoom.objects.create(user=self.request.user)
        serializer = ChatRoomSerializer(instance=room)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HeartbeatViewSet(viewsets.ViewSet):
    """
    Class representing a heartbeat viewset
    """
    http_method_names = ["get", "head", "options"]

    def list(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
