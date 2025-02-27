from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from apps.chat.models import ChatMessage, ChatFile, ChatRoom


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatFile
        fields = "__all__"

    def to_representation(self, value):
        data = super().to_representation(value)
        data["name"] = value.file_name()
        return data


class ChatMessageSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)
    user = UserDetailsSerializer()

    class Meta:
        model = ChatMessage
        fields = "__all__"


class ChatRoomSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()

    class Meta:
        model = ChatRoom
        fields = "__all__"
        read_only_fields = ("id", "user", "active")
