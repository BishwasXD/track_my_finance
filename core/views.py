from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView
from django.http import HttpResponse
from core.models import Income, Expense, Investment, Saving
from accounts.models import User
from core.serializers import (
    LineDataSerializer,
    PieDataSerializer,
    DonutSerializer,
    TableDataSerializer,
    AddTransactionSerializer,
)
import pandas as pd
from django.db.models.functions import TruncDate
from django.db.models import Sum
from core.utils import generatePieData
from itertools import chain
from operator import attrgetter
from django.db import models


class AddTransactionsView(APIView):
    """
    we need to pass in the dynamic field name for this api to work to the post method.
    unlike fn args the name should match the name from the url like: <str:type> corresponds to type here
    """

    def post(self, request, type):

        type_model_map = {
            "Income": Income,
            "Expense": Expense,
            "Investment": Investment,
            "Saving": Saving,
        }
        model = type_model_map.get(type)
        data = request.data.copy()
        # print(data)
        # data["user"] = self.request.user.id
        # print(data)
        serializer = AddTransactionSerializer(data=data)
        if serializer.is_valid():
            model.objects.create(**serializer.validated_data)
            return Response({"message": "Data added successfully"}, status=201)
        return Response(serializer.errors, status=400)


class GenerateCsvView(APIView):
    def get(self, request):
        income_data = Income.objects.all()
        df = pd.DataFrame(income_data)
        response = HttpResponse(content_type="text/csv")  # set content type in response
        response["Content-Disposition"] = (
            'attachment; filename="income_data.csv"'  # indicates atttached data is to be downloaded with given file name
        )
        df.to_csv(
            path_or_buf=response, index=False
        )  # directly writes csv data in response as the arg takes file path or a string

        return response


class IncomeExpenseLineChart(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        aggregated_income = (
            Income.objects.filter(user=user).values(Date=TruncDate("date"))
            # the annotate method groups the data by date(field specified in values method) and for each unique date it calculates the sum.
            # same dates are grouped together
            .annotate(amount=Sum("amount"))
            # sorting by date
            .order_by("Date")
        )
        aggregated_expense = (
            Expense.objects.filter(user=user)
            .values(Date=TruncDate("date"))
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
            line_data_response,
            status=200,
        )


def generate_format(data):
    res = {}
    for item in data:
        print(item)
        res[item["Date"]] = item["amount"]
    return res


class IncomeExpensePieChart(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        response = {}
        income_data = Income.objects.filter(user = user).order_by("amount")
        expense_data = Expense.objects.filter(user = user).order_by("amount")
        income_serializer = generatePieData(
            PieDataSerializer(income_data, many=True).data
        )
        expense_serializer = generatePieData(
            PieDataSerializer(expense_data, many=True).data
        )
        response["income"] = income_serializer
        response["expense"] = expense_serializer
        print('RES', response)
        return Response(response, status=200)


class IncomeExpenseDonutChart(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        print(user)
        income = Income.objects.filter(user=user)
        expense = Expense.objects.filter(user=user)
        income_data = sum_all(DonutSerializer(income, many=True).data, "Income")
        expense_data = sum_all(DonutSerializer(expense, many=True).data, "Expense")
        return Response(
            {
                "data": [income_data, expense_data],
                "message": "successfully loaded data",
            },
            status=200,
        )


def sum_all(data, label):
    total = 0
    for item in data:
        total = float(item["amount"]) + total
    return total


class TableSummaryDataView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        income_data = Income.objects.filter(user=user).annotate(
            field=models.Value("Income", output_field=models.CharField())
        )
        expense_data = Expense.objects.filter(user=user).annotate(
            field=models.Value("Expense", output_field=models.CharField())
        )
        combined_data = sorted(
            chain(income_data, expense_data), key=attrgetter("date"), reverse=True
        )
        table_data = TableDataSerializer(combined_data, many=True).data
        return Response(
            {"data": table_data, "message": "data loaded successfully"}, status=200
        )
