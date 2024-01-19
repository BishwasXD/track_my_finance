from django.urls import path

from core.views import UserIncomeView

urlpatterns = [
   path('add-income', UserIncomeView.as_view(), name = 'AddIncome')
]