from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import UserSerializer,UserLoginSerilaizer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

"""creates a new user in a database"""
class CreateUserView(APIView):
    def post(self, request):
        user = UserSerializer(data = request.data)
        user.is_valid(raise_exception = True)
        user.save()
        token = get_tokens_for_user(user)
        return Response({'message' : 'User Created Successfully!', 'token' : token},status=status.HTTP_201_CREATED)



class UserLoginView(APIView):
    def post(self, request):
        user = UserLoginSerilaizer(data = request.data)
        user.is_valid()
        email = user.data['email']
        password = user.data['password']

        """When you pass email=email as a keyword argument, you are explicitly stating that the value provided for authentication is the email."""
        user = authenticate(email = email, password = password)
        if user:
            token = get_tokens_for_user(user)
            return Response({'message' : 'User exists', 'token' : token}, status=status.HTTP_200_OK)
        return Response({'message' : 'Given user doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
        

