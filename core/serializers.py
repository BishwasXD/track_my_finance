from rest_framework import serializers

from core.models import Income, Expense, Budget
from accounts.models import User

class UserIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount','source','description', 'date']
    

class UserExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount','category','description','date', 'user']

class UserBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['amount', 'user']


class LineDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount']
    