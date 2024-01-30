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


class GetIncomeDetailsView(APIView):
    def get(self, request):
        income = Income.objects.filter(id = 11)
        serializer = UserIncomeSerializer(income, many = True)
        res = generateIncomeResponse(serializer)
        return Response(res, status=status.HTTP_202_ACCEPTED)

class GetExpenseDetailsView(APIView):
    def get(self, request):
        expense = Expense.objects.all()
        serializer = UserExpenseSerializer(expense, many = True)
        res = generateExpenseResponse(serializer)
        return Response(res, status=status.HTTP_202_ACCEPTED)


#TODO: change model field to category and use one fn to generate response
def generateIncomeResponse(serializer):
    response = {}
    res = {}
    for data in serializer.data:
       response[data['source']] = response.get(data['source'], 1) + float(data.get('amount'))

    sorted_keys = list(sorted(response, key = response.get, reverse=True))
    sorted_values = list(sorted(response.values(), reverse=True))

    if len(sorted_values) > 5:
     others_sum =sum(sorted_values[4:])
     res['others'] = others_sum

    for i in range(len(sorted_values)):
        res[sorted_keys[i]] = sorted_values[i]
        if i == 3:
            break
    return res



def generateExpenseResponse(serializer):
    response = {}
    res = {}
    for data in serializer.data:
       response[data['category']] = response.get(data['category'], 1) + float(data.get('amount'))

    sorted_keys = list(sorted(response, key = response.get, reverse=True))
    sorted_values = list(sorted(response.values(), reverse=True))

    if len(sorted_values) > 5:
     others_sum =sum(sorted_values[4:])
     res['others'] = others_sum

    for i in range(len(sorted_values)):
        res[sorted_keys[i]] = sorted_values[i]
        if i == 3:
            break
    return res