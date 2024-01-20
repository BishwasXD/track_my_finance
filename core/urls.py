from django.urls import path

from core.views import UserIncomeView, UserExpenseView, UserBudgetView

urlpatterns = [
   path('add-income', UserIncomeView.as_view(), name = 'AddIncome'),
   path('add-expense', UserExpenseView.as_view(), name='AddExpense'),
   path('add-budget', UserBudgetView.as_view(), name = 'AddBudget')
]