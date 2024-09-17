from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from accounts.serializers import UserSerializer, UserLoginSerilaizer
from accounts.models import User
from django.conf import settings


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class CreateUserView(APIView):
    def post(self, request):
        email = request.data["email"]
        if User.objects.filter(email=email).exists():
            return Response(
                {"message": "Email is already in use"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
            {"message": "User Created Successfully!", "token": token},
            status=201,
        )


class UserLoginView(APIView):
    def post(self, request):
        user = UserLoginSerilaizer(data=request.data)
        user.is_valid()
        email = user.data["email"]

        password = user.data["password"]

        """When you pass email=email as a keyword argument, you are explicitly stating that the value provided for authentication is the email."""
        user = authenticate(email=email, password=password)

        if user:
            token = get_tokens_for_user(user)
            return Response(
                {"message": "Logged in successfully", "token": token},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Invalid Login Details"}, status=status.HTTP_400_BAD_REQUEST
        )


# TODO: check token expiry later
class VerifyTokenView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"message": "Token not provided"}, 400)
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return Response(
            {"message": "Logged in successfully", "data": decoded_token}, 200
        )


class GoogleLoginView(APIView):
    def post(self, request):
        print("this is request data", request.data)
        google_email = request.data["email"]
        print(google_email)
        user, created = User.objects.get_or_create(email=google_email)
        print(user, created)
        token = get_tokens_for_user(user)
        return Response(
            {"message": "google User Created Successfully!", "token": token},
            status=status.HTTP_201_CREATED,
        )
