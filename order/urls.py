from django.urls import path
from .views import Payment

urlpatterns = [
	path('', Payment.as_view()),
]
