from django.db import models
from accounts.models import User


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add = True)
    category = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add = True)
    category = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    


    
