from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework import generics

from core.models import Income, Expense, Budget
from accounts.models import User
from core.serializers import UserIncomeSerializer, UserExpenseSerializer, UserBudgetSerializer


"""using APIView will transfer the request to the appropriate handler fn, like if the req type is post then post method inside view class shall handle that request"""
class UserIncomeView(APIView):
    def post(self, request):
        serializer = UserIncomeSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.data['amount']
        user = serializer.data['user']
        user_instance = User.objects.get(id=user)
        description = serializer.data['description']
        source = serializer.data['source']
        Income.objects.create(amount = amount, user = user_instance, description = description, source = source)
        return Response({'message' : 'income data added successfully!'}, status=status.HTTP_201_CREATED)


class UserExpenseView(APIView):
    def post(self, request):
      serializer = UserExpenseSerializer(data = request.data)
      serializer.is_valid(raise_exception=True)
      amount = serializer.data['amount']
      user = serializer.data['user']
      user_instance = User.objects.get(id=user)
      description = serializer.data['description']
      category = serializer.data['category']
      Expense.objects.create(amount = amount, user = user_instance, description = description, category = category)
      return Response({'message' : 'expense data added successfully!'}, status=status.HTTP_201_CREATED)

class UserBudgetView(APIView):
    def post(self, request):
        serializer = UserBudgetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.data['amount']
        user = serializer.data['user']
        user_instance = User.objects.get(id=user)
        Budget.objects.create(amount = amount, user = user_instance)
        return Response({'message' : 'budget data added successfully!'}, status=status.HTTP_201_CREATED)

