from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'
    TYPE_CHOICES = [(INCOME, 'Income'), (EXPENSE, 'Expense')]

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.amount} ({self.category.name})"

class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0')) # error bez Decimal()
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"