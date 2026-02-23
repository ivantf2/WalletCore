from django.urls import path
from . import views

app_name = "finances"

urlpatterns = [
    path("register/", views.register, name="register"),

    # Categories
    path("categories/", views.CategoryList.as_view(), name="category_list"),
    path("categories/new/", views.CategoryCreate.as_view(), name="category_create"),
    path("categories/<int:pk>/", views.CategoryDetail.as_view(), name="category_detail"),
    path("categories/<int:pk>/edit/", views.CategoryUpdate.as_view(), name="category_edit"),
    path("categories/<int:pk>/delete/", views.CategoryDelete.as_view(), name="category_delete"),

    # Transactions
    path("transactions/", views.TransactionList.as_view(), name="transaction_list"),
    path("transactions/new/", views.TransactionCreate.as_view(), name="transaction_create"),
    path("transactions/<int:pk>/", views.TransactionDetail.as_view(), name="transaction_detail"),
    path("transactions/<int:pk>/edit/", views.TransactionUpdate.as_view(), name="transaction_edit"),
    path("transactions/<int:pk>/delete/", views.TransactionDelete.as_view(), name="transaction_delete"),

    # Goals
    path("goals/", views.GoalList.as_view(), name="goal_list"),
    path("goals/new/", views.GoalCreate.as_view(), name="goal_create"),
    path("goals/<int:pk>/", views.GoalDetail.as_view(), name="goal_detail"),
    path("goals/<int:pk>/edit/", views.GoalUpdate.as_view(), name="goal_edit"),
    path("goals/<int:pk>/delete/", views.GoalDelete.as_view(), name="goal_delete"),
]