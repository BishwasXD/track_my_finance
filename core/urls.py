from django.urls import path

from core.views import (
    UserIncomeView,
    UserExpenseView,
    UserBudgetView,
    GenerateCsvView,
    IncomeExpenseLineChart,
    IncomeExpensePieChart
)

urlpatterns = [
    path("add-income", UserIncomeView.as_view(), name="AddIncome"),
    path("add-expense", UserExpenseView.as_view(), name="AddExpense"),
    path("add-budget", UserBudgetView.as_view(), name="AddBudget"),
    path("get-csv-file", GenerateCsvView.as_view(), name="generate-csv"),
    path('get-line-chart', IncomeExpenseLineChart.as_view(), name='get-line-chart'),
    path('get-pie-chart', IncomeExpensePieChart.as_view(), name='pie-chart')
]
