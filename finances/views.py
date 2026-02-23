from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .models import Category, Transaction, FinancialGoal
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import TransactionForm, CategoryForm, GoalForm
from django.db.models import Sum

# Create your views here.

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = "finances/category_list.html"

class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "finances/category_detail.html"

class TransactionList(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "finances/transaction_list.html"

    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user).select_related("category")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(note__icontains=q) | Q(category__name__icontains=q))
        return qs.order_by("-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        total_income = qs.filter(category__type=Category.INCOME).aggregate(
            total=Sum("amount")
        )["total"] or 0

        total_expense = qs.filter(category__type=Category.EXPENSE).aggregate(
            total=Sum("amount")
        )["total"] or 0

        context["total_income"] = total_income
        context["total_expense"] = total_expense
        context["balance"] = total_income - total_expense

        return context

class TransactionDetail(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "finances/transaction_detail.html"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class GoalList(LoginRequiredMixin, ListView):
    model = FinancialGoal
    template_name = "finances/goal_list.html"

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user).order_by("deadline")

class GoalDetail(LoginRequiredMixin, DetailView):
    model = FinancialGoal
    template_name = "finances/goal_detail.html"

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("finances:transaction_list")  # ili gdje želiš
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")

class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "finances/transaction_form.html"
    success_url = reverse_lazy("finances:transaction_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "finances/transaction_form.html"
    success_url = reverse_lazy("finances:transaction_list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "finances/transaction_confirm_delete.html"
    success_url = reverse_lazy("finances:transaction_list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "finances/category_form.html"
    success_url = reverse_lazy("finances:category_list")

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "finances/category_form.html"
    success_url = reverse_lazy("finances:category_list")

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "finances/category_confirm_delete.html"
    success_url = reverse_lazy("finances:category_list")
    
class GoalCreate(LoginRequiredMixin, CreateView):
    model = FinancialGoal
    form_class = GoalForm
    template_name = "finances/goal_form.html"
    success_url = reverse_lazy("finances:goal_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdate(LoginRequiredMixin, UpdateView):
    model = FinancialGoal
    form_class = GoalForm
    template_name = "finances/goal_form.html"
    success_url = reverse_lazy("finances:goal_list")

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)

class GoalDelete(LoginRequiredMixin, DeleteView):
    model = FinancialGoal
    template_name = "finances/goal_confirm_delete.html"
    success_url = reverse_lazy("finances:goal_list")

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)