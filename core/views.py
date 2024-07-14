from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework import generics
from django.http import HttpResponse
from core.models import Income, Expense, Budget
from accounts.models import User
from core.serializers import (
    UserIncomeSerializer,
    UserExpenseSerializer,
    UserBudgetSerializer,
    LineDataSerializer,
)
import pandas as pd


class UserIncomeView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data.copy()
        data["user"] = self.request.user.id
        serializer = UserIncomeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Income data added successfully"}, status=201)


class UserExpenseView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        data = request.data.copy()
        data["user"] = self.request.user.id
        serializer = UserExpenseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message",
                f"Expense data added successfully for a user {self.request.user}",
            },
            status=201,
        )


class UserBudgetView(APIView):
    def post(self, request):
        serializer = UserBudgetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.data["amount"]
        user = serializer.data["user"]
        user_instance = User.objects.get(id=user)
        Budget.objects.create(amount=amount, user=user_instance)
        return Response(
            {"message": "budget data added successfully!"},
            status=status.HTTP_201_CREATED,
        )


class GetIncomeDetailsView(APIView):
    def get(self, request):
        income = Income.objects.all()
        serializer = UserIncomeSerializer(income, many=True)
        res = generateDoughnutData(serializer)
        return Response(res, status=status.HTTP_202_ACCEPTED)


class GetExpenseDetailsView(APIView):
    def get(self, request):
        user = self.request.user.id
        expense = Expense.objects.get(user_id=user)
        serializer = UserExpenseSerializer(expense, many=True)
        res = generateDoughnutData(serializer, True)
        return Response(res, status=status.HTTP_202_ACCEPTED)



class GenerateCsvView(APIView):
    def get(self, request):

        income_data = Income.objects.all()

        income_serializer = UserIncomeSerializer(income_data, many=True).data

        df = pd.DataFrame(income_serializer)

        response = HttpResponse(content_type="text/csv")  # set content type in response

        response["Content-Disposition"] = (
            'attachment; filename="income_data.csv"'  # indicates atttached data is to be downloaded with given file name
        )

        df.to_csv(
            path_or_buf=response, index=False
        )  # directly writes csv data in response as the arg takes file path or a string

        return response


def generateDoughnutData(serializer, expense=None):
    response = {}
    res = {}

    if expense is not None:
        for data in serializer.data:
            response[data["category"]] = response.get(data["category"], 0) + float(
                data.get("amount")
            )
    else:
        for data in serializer.data:
            response[data["source"]] = response.get(data["source"], 0) + float(
                data.get("amount")
            )

    sorted_keys = list(sorted(response, key=response.get, reverse=True))
    sorted_values = list(sorted(response.values(), reverse=True))

    if len(sorted_values) > 5:
        others_sum = sum(sorted_values[4:])
        res["others"] = others_sum

    for i in range(len(sorted_values)):
        res[sorted_keys[i]] = sorted_values[i]
        if i == 3:
            break
    return res


def generate(data:object):
    res = {}
    for key, value in data.items():
        res[key] += (value, 0)
    for key, value in res.items():
        pass
        
    
        

