from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .models import Category, Transaction, FinancialGoal

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