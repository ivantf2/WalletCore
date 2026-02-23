from django import forms
from .models import Transaction
from .models import Category, FinancialGoal


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["category", "amount", "date", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "type"]
        
class GoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ["title", "target_amount", "current_amount", "deadline"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }