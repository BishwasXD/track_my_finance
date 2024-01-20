from rest_framework import serializers

from core.models import Income, Expense, Budget
from accounts.models import User

class UserIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount','source','description','user']
    

class UserExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount','category','description','user']

class UserBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['amount', 'user']
        