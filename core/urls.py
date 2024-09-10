from django.urls import path

from core.views import (
    UserIncomeView,
    UserExpenseView,
    GenerateCsvView,
    IncomeExpenseLineChart,
    IncomeExpensePieChart,
    IncomeExpenseDonutChart,
    TableSummaryDataView
    
)

urlpatterns = [
    path("add-income", UserIncomeView.as_view(), name="AddIncome"),
    path("add-expense", UserExpenseView.as_view(), name="AddExpense"),
    path("get-csv-file", GenerateCsvView.as_view(), name="generate-csv"),
    path('get-line-chart', IncomeExpenseLineChart.as_view(), name='get-line-chart'),
    path('get-pie-chart', IncomeExpensePieChart.as_view(), name='pie-chart'),
    path('get-donut-chart', IncomeExpenseDonutChart.as_view(), name='donut-chart'),
    path('get-summarytable-data',TableSummaryDataView.as_view(),name='table-suumary')
]
