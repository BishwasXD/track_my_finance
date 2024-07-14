from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta

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
    source = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Budget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default= timezone.now() + timedelta(days=30))

    
