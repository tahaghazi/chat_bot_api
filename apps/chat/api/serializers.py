from rest_framework import serializers

from apps.chat.models import ChatMessage, ChatFile


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

    class Meta:
        model = ChatMessage
        fields = "__all__"
