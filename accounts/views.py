from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserSignupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ParseError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class UserSignupView(APIView):
    def post(self, request):
        try:
            serializer = UserSignupSerializer(data=request.data)
        except ParseError:
            return Response(
                {'detail': 'Malformed request.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
