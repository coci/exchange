from django.urls import path
from .views import AdditionUserBalanceApi

urlpatterns = [
	path("",AdditionUserBalanceApi.as_view()),
]