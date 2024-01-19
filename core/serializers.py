from rest_framework import serializers

from core.models import Income, Expense, Budget
from accounts.models import User

class UserIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount','source','description','user']
    

