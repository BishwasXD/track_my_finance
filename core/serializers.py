from rest_framework import serializers

from core.models import Income, Expense
from accounts.models import User

class UserIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount','category','description', 'date']
    

class UserExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount','category','description','date', 'user']

class LineDataSerializer(serializers.Serializer):
    Date = serializers.DateField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class PieDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount', 'category']
 

class DonutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount']

class TableDataSerializer(serializers.ModelSerializer):
    field = serializers.CharField()
    class Meta:
        model = Income
        fields = "__all__"