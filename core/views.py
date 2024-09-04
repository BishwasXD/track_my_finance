from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import APIView
from django.http import HttpResponse
from core.models import Income, Expense, Budget
from accounts.models import User
from core.serializers import (
    UserIncomeSerializer,
    UserExpenseSerializer,
    UserBudgetSerializer,
    LineDataSerializer,
    PieDataSerializer,
)
import pandas as pd
from django.db.models.functions import TruncDate
from django.db.models import Sum
from core.utils import generatePieData


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


class IncomeExpenseLineChart(APIView):

    def get(self, request):
        aggregated_income = (
            Income.objects.values(Date=TruncDate("date"))
            # the annotate method groups the data by date(field specified in values method) and for each unique date it calculates the sum.
            # same dates are grouped together
            .annotate(amount=Sum("amount"))
            # sorting by date
            .order_by("Date")
        )
        aggregated_expense = (
            Expense.objects.values(Date=TruncDate("date"))
            .annotate(amount=Sum("amount"))
            .order_by("Date")
        )

        income_serializer = generate_format(
            LineDataSerializer(aggregated_income, many=True).data
        )
        expense_serializer = generate_format(
            LineDataSerializer(aggregated_expense, many=True).data
        )

        line_data_response = {
            "income": income_serializer,
            "expense": expense_serializer,
        }

        return Response(
            {"data": line_data_response, "message": "data loaded successfully"},
            status=200,
        )


def generate_format(data):
    res = {}
    for item in data:
        print(item)
        res[item["Date"]] = item["amount"]
    return res


class IncomeExpensePieChart(APIView):
    def get(self, request):
        response = {}
        income_data = Income.objects.order_by("amount")
        expense_data = Expense.objects.order_by("amount")
        income_serializer = generatePieData(
            PieDataSerializer(income_data, many=True).data
        )
        expense_serializer = generatePieData(
            PieDataSerializer(expense_data, many=True).data
        )
        response["income_data"] = income_serializer
        response["expense_data"] = expense_serializer
        return Response(
            {"data": response, "message": "Data loaded successfully"}, status=200
        )
