from django.db import models
from accounts.models import User


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Expense(Transaction):
    pass

class Income(Transaction):
    pass

class Investment(Transaction):
    pass

class Saving(Transaction):
    pass
