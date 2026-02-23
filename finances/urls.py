from django.urls import path
from . import views

app_name = "finances"

urlpatterns = [
    path("register/", views.register, name="register"),
    
    path("categories/", views.CategoryList.as_view(), name="category_list"),
    path("categories/<int:pk>/", views.CategoryDetail.as_view(), name="category_detail"),

    path("transactions/", views.TransactionList.as_view(), name="transaction_list"),
    path("transactions/<int:pk>/", views.TransactionDetail.as_view(), name="transaction_detail"),

    path("goals/", views.GoalList.as_view(), name="goal_list"),
    path("goals/<int:pk>/", views.GoalDetail.as_view(), name="goal_detail"),
]