from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User, related_name="account",on_delete=models.CASCADE)
    account_id = models.IntegerField(unique=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=100)
    


    def __str__(self):
        return f"{self.user} ({self.account_id})"


class Deposit(models.Model):
    account = models.ForeignKey(UserLibraryAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after_deposit = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

