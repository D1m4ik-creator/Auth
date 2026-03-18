from django.contrib.auth import authenticate
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, LogoutSerializer, UserRegisterSerializer, UserSerializer

class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Регистрация нового пользователя",
        description="Принимает данные пользователя, создает аккаунт и возвращает JWT токены.",
        request=UserRegisterSerializer,
        responses={
            201: OpenApiResponse(
                description="Успешная регистрация",
                response=UserSerializer
            ),
            400: OpenApiResponse(description="Ошибка валидации данных")
        },
        tags=["Аутентификация"]
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Авторизация пользователя",
        description="Принимает данные пользователя и возвращает JWT токены.",
        request=LoginSerializer,
        responses={
            201: OpenApiResponse(
                description="Успешная аутентификация",
            ),
            400: OpenApiResponse(description="Ошибка валидации данных")
        },
        tags=["Аутентификация"]  # Группирует эндпоинты в интерфейсе
    )
    def post(self, request):
        data = request.data
        email = data.get("email", None)
        username = data.get('username', None)
        password = data.get('password', None)

        if email is None or password is None:
            return Response({'error': 'Нужен и логин, и пароль'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Выход из системы (отзыв токена)",
        description="Принимает refresh токен и заносит его в черный список. После этого токен станет недействительным.",
        request=LogoutSerializer,
        responses={
            205: OpenApiResponse(description="Успешный выход, токен отозван"),
            400: OpenApiResponse(description="Неверный или просроченный токен"),
            401: OpenApiResponse(description="Пользователь не авторизован")
        },
        tags=["Аутентификация"]
    )

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)
