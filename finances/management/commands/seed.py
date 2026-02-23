from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from finances.models import Category, Transaction, FinancialGoal
from finances.factories import UserFactory, CategoryFactory, TransactionFactory, FinancialGoalFactory

NUM_USERS = 3
NUM_CATEGORIES = 8
NUM_TRANSACTIONS = 40
NUM_GOALS = 6

class Command(BaseCommand):
    help = "Seed test data for WalletCore"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Transaction.objects.all().delete()
        FinancialGoal.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("Creating users...")
        for _ in range(NUM_USERS):
            UserFactory()

        self.stdout.write("Creating categories...")
        for _ in range(NUM_CATEGORIES):
            CategoryFactory()

        self.stdout.write("Creating transactions...")
        for _ in range(NUM_TRANSACTIONS):
            TransactionFactory()

        self.stdout.write("Creating goals...")
        for _ in range(NUM_GOALS):
            FinancialGoalFactory()

        self.stdout.write(self.style.SUCCESS("Seed complete "))