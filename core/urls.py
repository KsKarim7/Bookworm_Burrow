from .views import UserRegistrationView
from django.urls import path,include

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name = 'register'),
]