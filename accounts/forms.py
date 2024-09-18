from django.contrib.auth.forms import UserCreationForm
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from django import forms
from .models import UserLibraryAccount
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date'}))
    address = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username','password1','password2','first_name','last_name','email','birth_date','address']
    
    def save(self,commit=True):
        user = super().save(commit = False)
        if(commit == True):
            user.save()
            UserLibraryAccount.objects.create(user=user, account_id=user.id, birth_date=self.cleaned_data['birth_date'], address=self.cleaned_data['address'],account_no = 2230109 + user.id)
            return user