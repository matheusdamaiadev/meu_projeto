from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProjectSerializer
)

from .models import Project



class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]



class MeView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)



class ProjectViewSet(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        return Project.objects.filter(
            user=self.request.user
        )


    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )