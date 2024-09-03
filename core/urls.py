from django.urls import path

from core.views import (
    UserIncomeView,
    UserExpenseView,
    UserBudgetView,
    GetExpenseDetailsView,
    GetIncomeDetailsView,
    GenerateCsvView,
    IncomeExpenseLineChart,
)

urlpatterns = [
    path("add-income", UserIncomeView.as_view(), name="AddIncome"),
    path("add-expense", UserExpenseView.as_view(), name="AddExpense"),
    path("add-budget", UserBudgetView.as_view(), name="AddBudget"),
    path("get-income-details", GetIncomeDetailsView.as_view(), name="GetIncome"),
    path("get-expense-details", GetExpenseDetailsView.as_view(), name="GetExpense"),
    path("get-csv-file", GenerateCsvView.as_view(), name="generate-csv"),
    path('get-line-chart', IncomeExpenseLineChart.as_view(), name='get-line-chart')
]
