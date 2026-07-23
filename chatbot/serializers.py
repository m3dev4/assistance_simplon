from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    question = serializers.CharField()