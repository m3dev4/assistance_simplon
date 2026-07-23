from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import ChatSerializer
from ingestion import ask_question


class ChatViewSet(ViewSet):

    def create(self, request):

        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]

        response = ask_question(question)

        return Response(
            {"answer": response["answer"]},
            status=status.HTTP_200_OK,
        )
