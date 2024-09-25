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
    BarDataSerializer,
)
import pandas as pd
from django.db.models.functions import TruncDate
from django.db.models import Sum
from core.utils import generatePieData
from itertools import chain
from operator import attrgetter
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class AddTransactionsView(APIView):
    """
    we need to pass in the dynamic field name for this api to work to the post method.
    unlike fn args the name should match the name from the url like: <str:type> corresponds to type here
    """
    type_model_map = {
            "Income": Income,
            "Expense": Expense,
            "Investment": Investment,
            "Saving": Saving,
        }
    def post(self, request, type):

      
        model = self.type_model_map.get(type)
        serializer = AddTransactionSerializer(data=request.data)
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
            LineDataSerializer(aggregated_income, many=True).data, "Date"
        )
        expense_serializer = generate_format(
            LineDataSerializer(aggregated_expense, many=True).data, "Date"
        )

        line_data_response = {
            "income": income_serializer,
            "expense": expense_serializer,
        }

        return Response(
            line_data_response,
            status=200,
        )


def generate_format(data, key):
    res = {}
    for item in data:
        res[item[key]] = item["amount"]
    return res


class IncomeExpensePieChart(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        response = {}
        income_data = Income.objects.filter(user=user).order_by("amount")
        expense_data = Expense.objects.filter(user=user).order_by("amount")
        income_serializer = generatePieData(
            PieDataSerializer(income_data, many=True).data
        )
        expense_serializer = generatePieData(
            PieDataSerializer(expense_data, many=True).data
        )
        response["income"] = income_serializer
        response["expense"] = expense_serializer
        print("RES", response)
        return Response(response, status=200)


from datetime import datetime


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


class SummaryCardDataView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        income_amount = Income.objects.filter(user=user).aggregate(
            income_amount=Sum("amount")
        )
        expense_amount = Expense.objects.filter(user=user).aggregate(
            expense_amount=Sum("amount")
        )
        investment_amount = Investment.objects.filter(user=user).aggregate(
            investment_amount=Sum("amount")
        )
        saving_amount = Saving.objects.filter(user=user).aggregate(
            saving_amount=Sum("amount")
        )

        response_data = {
            "income_amount": income_amount["income_amount"] or 0,
            "expense_amount": expense_amount["expense_amount"] or 0,
            "investment_amount": investment_amount["investment_amount"] or 0,
            "saving_amount": saving_amount["saving_amount"] or 0,
        }

        return Response(response_data)


class BarChartDataView(APIView):
    days_map = {
        "weekly": 7,
        "monthly": 30,
        "yearly": 360,
    }

    # what we need to do is to filter the data by time and add the data from that particular time frame.
    # for income first we need to find the first entry and the last entry.
    # then divide the time frame lets say if time frame is 1 yr 3 month, and filter is weekly it gets divided into, 60ish  part.
    # iterate 60 times, accumulate data and add on list, there will be 60 data points can be messy in the chart.
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request, filter):
        filter = 30
        user = request.user

        expense_data = Expense.objects.filter(user = user).order_by("date")
        income_data = Income.objects.filter(user = user).order_by("date")
        investment_data = Investment.objects.filter(user = user).order_by("date")
        saving_data = Saving.objects.filter(user = user).order_by("date")
        expense_data = generate_format(
            BarDataSerializer(expense_data, many=True).data, "date"
        )
        income_data = generate_format(
            BarDataSerializer(income_data, many=True).data, "date"
        )
        investment_data = generate_format(
            BarDataSerializer(investment_data, many=True).data, "date"
        )
        saving_data = generate_format(
            BarDataSerializer(saving_data, many=True).data, "date"
        )

        expense_bardata = self.return_bardata(expense_data, filter)
        income_bardata = self.return_bardata(income_data, filter)
        investment_bardata = self.return_bardata(investment_data, filter)
        saving_bardata = self.return_bardata(saving_data, filter)

        response_data = {
            "expenses": expense_bardata,
            "income": income_bardata,
            "investments": investment_bardata,
            "savings": saving_bardata,
        }

        return Response(response_data)

    def return_bardata(self, data, filter):
        def parse_datetime(date_str):
            try:

                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:

                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z").replace(
                    tzinfo=timezone.utc
                )

        keys = [parse_datetime(date_str) for date_str in data.keys()]

        values = list(data.values())
        p1 = 0
        p2 = 1
        res = {}
        while p2 < len(values):
            difference = (keys[p2] - keys[p1]).days
            if difference >= filter:
                res[p1] = values[p1]
                p1 = p1 + 1
                p2 = p2 + 1

            elif difference < filter:
                sum = float(values[p1])
                while p2 < len(keys) and (keys[p2] - keys[p1]).days < filter:
                    sum = sum + float(values[p2])
                    p2 = p2 + 1
                res[p1] = sum
                p1 = p2
                p2 = p2 + 1
        if p1 == len(values) - 1:
            res[p1] = values[p1]

        return res

class EditTransactionDataView(APIView):
    type_model_map = {
            "Income": Income,
            "Expense": Expense,
            "Investment": Investment,
            "Saving": Saving,
        }
    def put(self, request, id, type):
        model = self.type_model_map.get(type)
        try:
            txn = model.objects.get(id = id)
        except ObjectDoesNotExist:
            return Response({'message':'No transaction recorded with given id.'}, 400)
        serializer = AddTransactionSerializer(instance = txn,data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message' : 'Transaction edited successfully!'}, 201)

        
    def delete(self, request, id, type):
        model = self.type_model_map.get(type)
        try:
            txn = model.objects.get(id = id)
            txn.delete()
            return Response({'message':'Transaction deeted successfully'}, status=200)
        except ObjectDoesNotExist:
            return Response({'message':'No transaction recorded with given id.'}, 400)

        