from django.urls import path

from core.views import (
    GenerateCsvView,
    IncomeExpenseLineChart,
    IncomeExpensePieChart,
    IncomeExpenseDonutChart,
    TableSummaryDataView,
    AddTransactionsView,
    SummaryCardDataView,
    BarChartDataView,
    EditTransactionDataView
    
)

urlpatterns = [
    path("get-csv-file", GenerateCsvView.as_view(), name="generate-csv"),
    path('get-line-chart', IncomeExpenseLineChart.as_view(), name='get-line-chart'),
    path('get-pie-chart', IncomeExpensePieChart.as_view(), name='pie-chart'),
    path('get-donut-chart', IncomeExpenseDonutChart.as_view(), name='donut-chart'),
    path('get-summarytable-data',TableSummaryDataView.as_view(),name='table-suumary'),
    path('add-transaction/<str:type>/', AddTransactionsView.as_view(),name='add-transaction'),
    path('get-summary-data', SummaryCardDataView.as_view(), name='summary-data'),
    path('get-bar-chart/<str:filter>/', BarChartDataView.as_view(), name='bar-chart'),
    path('edit-transaction-data/<int:id>/<str:type>/', EditTransactionDataView.as_view(), name='edit-transaction')
]
