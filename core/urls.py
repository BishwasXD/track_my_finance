from django.urls import path

from core.views import UserIncomeView, UserExpenseView, UserBudgetView, GetExpenseDetailsView,GetIncomeDetailsView

urlpatterns = [
   path('add-income', UserIncomeView.as_view(), name = 'AddIncome'),
   path('add-expense', UserExpenseView.as_view(), name='AddExpense'),
   path('add-budget', UserBudgetView.as_view(), name = 'AddBudget'),
   path('get-income-details',GetIncomeDetailsView.as_view(), name='GetIncome'),
   path('get-expense-details',GetExpenseDetailsView.as_view(), name='GetExpense')
]