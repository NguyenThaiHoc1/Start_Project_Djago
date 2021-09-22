from django.urls import path
from .views import RegistrationAPIView
from . import views

app_name = 'authentication'

urlpatterns = [
    path('users/', RegistrationAPIView.as_view(), name="register"),
    path('test/', views.vote, name="test")
]