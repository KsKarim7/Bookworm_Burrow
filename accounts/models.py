from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User, related_name="account",on_delete=models.CASCADE)
    account_id = models.IntegerField(unique=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    balance = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} ({self.account_id})"
