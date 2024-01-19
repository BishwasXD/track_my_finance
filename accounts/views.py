from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import UserSerializer


"""creates a new user in a database"""
class CreateUserView(APIView):
    def post(self, request):
        user = UserSerializer(data = request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response({'message' : 'User Created Successfully!'},status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    pass