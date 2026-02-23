import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Transaction, FinancialGoal
import random

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker("user_name")

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker("word")
    type = factory.Iterator([Category.INCOME, Category.EXPENSE])

class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction
    user = factory.Iterator(User.objects.all())
    category = factory.Iterator(Category.objects.all())
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    date = factory.LazyFunction(lambda: timezone.now().date())
    note = factory.Faker("sentence")

class FinancialGoalFactory(DjangoModelFactory):
    class Meta:
        model = FinancialGoal
    user = factory.Iterator(User.objects.all())
    title = factory.Faker("sentence", nb_words=3)
    target_amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    current_amount = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    deadline = factory.Faker("date_this_year")