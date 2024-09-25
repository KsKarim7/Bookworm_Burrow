from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserLogoutView,DepositView
from django.urls import path,include
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    # path('deposit/', views.deposit_money, name='deposit_money'),
    path('profile/',  views.profileView, name='profile'),

]