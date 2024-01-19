from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta

from accounts.models import User


class Source(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    description = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add = True)
    source = models.ForeignKey(Source, on_delete = models.CASCADE)
    description = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Budget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    user = user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default= timezone.now() + timedelta(days=30))

    
