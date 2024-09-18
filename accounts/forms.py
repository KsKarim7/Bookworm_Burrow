from django.contrib.auth.forms import UserCreationForm
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
            UserLibraryAccount.objects.create(user=user, account_id=2230109 + user.id, birth_date=self.cleaned_data['birth_date'], address=self.cleaned_data['address'])
            return user
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })
