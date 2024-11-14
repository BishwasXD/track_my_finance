from rest_framework import serializers

from core.models import Transaction, Income


"""
apparently we cannot use Transcation as a model because it is a abstract model from which other models are derived
and it has no corresponding table in the database and django tries to map the value to correspondig field in the table
for eg: we often use serializer.save() to save val directly to database 
"""
class AddTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"

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

class BarDataSerializer(serializers.Serializer):
    month = serializers.DateTimeField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class ReportSerializer(serializers.Serializer):
    total_transactions = serializers.IntegerField()
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
