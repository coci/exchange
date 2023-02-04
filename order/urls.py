from django.urls import path

from .views import MakeOrderAPI

urlpatterns = [
	path('', MakeOrderAPI.as_view()),
]
