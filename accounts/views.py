from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import DepositForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Deposit,UserLibraryAccount
from django.contrib import messages
from posts.models import BorrowedBookModel

# INSERT INTO userlibraryaccount (user_id, account_id, birth_date, balance, address)
# VALUES (<user_id>, <unique_account_id>, NULL, 0.00, 'Default Address');

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        # print(form.cleaned_data)
        user = form.save() 
        login(self.request, user)
        return super().form_valid(form)
    
# SELECT * 
# FROM auth_user
# WHERE username = 'provided_username_or_email'
# LIMIT 1;

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
    
# DELETE FROM django_session
# WHERE session_key = '<current_session_key>';

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    

# SELECT * 
# FROM userlibraryaccount
# WHERE user_id = <current_user_id>;
# UPDATE userlibraryaccount
# SET balance = balance + <deposit_amount>
# WHERE id = <account_id>;
# INSERT INTO deposit (account_id, amount, balance_after_deposit, timestamp)
# VALUES (<account_id>, <deposit_amount>, <updated_balance>, NOW());

class DepositView(LoginRequiredMixin, View):
    template_name = 'accounts/deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('home')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = request.user.account
            account.balance += amount
            account.save()
            Deposit.objects.create(account=account, amount=amount)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
    


# SELECT * 
# FROM userlibraryaccount
# WHERE user_id = <current_user_id>;

def profileView(request):

    data = BorrowedBookModel.objects.filter(user=request.user)
    user_data = UserLibraryAccount.objects.filter(user=request.user)

    
    return render(request, 'accounts/profile.html', {'data':data, 'user_data':user_data})