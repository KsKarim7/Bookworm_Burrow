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


class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        # print(form.cleaned_data)
        user = form.save() 
        login(self.request, user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    

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
    
# def deposit_money(request):
#     user_account = request.user.account  
    
#     if request.method == 'POST':
#         form = DepositForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             user_account.balance += amount
#             user_account.save()
#             messages.success(
#             request,
#             f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
#             )

#             # send_transaction_email(request.user, amount, "Deposit Message", "deposit_mail.html")
#             return redirect('home')  
        

#     else:
#         form = DepositForm()

#     return render(request, 'deposit_money.html', {'form': form})

def profileView(request):
    # data1 = User.objects.filter(user=request.user)
    # print(data1)
    data = BorrowedBookModel.objects.filter(user=request.user)
    user_data = UserLibraryAccount.objects.filter(user=request.user)
    # print(user_data)
    # for i in user_data:
    #     print(i.balance)
    # print(object)
    
    return render(request, 'accounts/profile.html', {'data':data, 'user_data':user_data})