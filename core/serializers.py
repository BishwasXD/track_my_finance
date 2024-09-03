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


from rest_framework import serializers

class LineDataSerializer(serializers.Serializer):
    Date = serializers.DateField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
 

    