from django.urls import path

from core.views import UserIncomeView, UserExpenseView, UserBudgetView, GetExpenseDetailsView,GetIncomeDetailsView, GetIncomeExpenseView, GenerateCsvView

urlpatterns = [
   path('add-income', UserIncomeView.as_view(), name = 'AddIncome'),
   path('add-expense', UserExpenseView.as_view(), name='AddExpense'),
   path('add-budget', UserBudgetView.as_view(), name = 'AddBudget'),
   path('get-income-details',GetIncomeDetailsView.as_view(), name='GetIncome'),
   path('get-expense-details',GetExpenseDetailsView.as_view(), name='GetExpense'),
   path('get-linechart-data',GetIncomeExpenseView.as_view(),name='linechart'),
   path('get-csv-file', GenerateCsvView.as_view(), name='generate-csv')
]