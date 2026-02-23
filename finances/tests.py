from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

from .models import Category, Transaction, FinancialGoal


class AuthAndPermissionsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="u1", password="pass12345")
        self.user2 = User.objects.create_user(username="u2", password="pass12345")

        self.cat_income = Category.objects.create(name="Salary", type=Category.INCOME)
        self.cat_expense = Category.objects.create(name="Food", type=Category.EXPENSE)

        self.t1 = Transaction.objects.create(
            user=self.user1,
            category=self.cat_expense,
            amount=Decimal("12.50"),
            date=timezone.now().date(),
            note="u1 txn",
        )
        self.t2 = Transaction.objects.create(
            user=self.user2,
            category=self.cat_income,
            amount=Decimal("100.00"),
            date=timezone.now().date(),
            note="u2 txn",
        )

        self.g1 = FinancialGoal.objects.create(
            user=self.user1,
            title="New PC",
            target_amount=Decimal("1500.00"),
            current_amount=Decimal("200.00"),
        )
        self.g2 = FinancialGoal.objects.create(
            user=self.user2,
            title="Trip",
            target_amount=Decimal("800.00"),
            current_amount=Decimal("50.00"),
        )

    def test_transactions_list_requires_login(self):
        resp = self.client.get(reverse("finances:transaction_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp["Location"])

    def test_goals_list_requires_login(self):
        resp = self.client.get(reverse("finances:goal_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login/", resp["Location"])

    def test_logged_in_user_sees_only_their_transactions(self):
        self.client.login(username="u1", password="pass12345")
        resp = self.client.get(reverse("finances:transaction_list"))
        self.assertEqual(resp.status_code, 200)
        # u1 transaction is visible
        self.assertContains(resp, "u1 txn")
        # u2 transaction is not visible
        self.assertNotContains(resp, "u2 txn")

    def test_transaction_detail_for_other_user_is_404(self):
        self.client.login(username="u1", password="pass12345")
        resp = self.client.get(reverse("finances:transaction_detail", args=[self.t2.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_goal_detail_for_other_user_is_404(self):
        self.client.login(username="u1", password="pass12345")
        resp = self.client.get(reverse("finances:goal_detail", args=[self.g2.pk]))
        self.assertEqual(resp.status_code, 404)

    def test_create_transaction_sets_user_automatically(self):
        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(
            reverse("finances:transaction_create"),
            data={
                "category": self.cat_expense.pk,
                "amount": "9.99",
                "date": str(timezone.now().date()),
                "note": "created by test",
            },
        )
        self.assertEqual(resp.status_code, 302)
        created = Transaction.objects.get(note="created by test")
        self.assertEqual(created.user, self.user1)

    def test_create_goal_sets_user_automatically(self):
        self.client.login(username="u1", password="pass12345")
        resp = self.client.post(
            reverse("finances:goal_create"),
            data={
                "title": "Goal X",
                "target_amount": "100.00",
                "current_amount": "0.00",
                "deadline": "",
            },
        )
        self.assertEqual(resp.status_code, 302)
        created = FinancialGoal.objects.get(title="Goal X")
        self.assertEqual(created.user, self.user1)


class ModelStringTests(TestCase):
    def test_str_methods(self):
        user = User.objects.create_user(username="k", password="pass12345")
        cat = Category.objects.create(name="Food", type=Category.EXPENSE)
        txn = Transaction.objects.create(user=user, category=cat, amount=Decimal("1.00"))
        goal = FinancialGoal.objects.create(user=user, title="Laptop", target_amount=Decimal("10.00"))

        self.assertIn("Food", str(cat))
        self.assertIn("k", str(txn))
        self.assertIn("Laptop", str(goal))