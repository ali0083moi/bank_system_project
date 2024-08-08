from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BankAccount(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bank_accounts'
    )
    account_number = models.CharField(max_length=16, unique=True, primary_key=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.account_number} - {self.owner.id_number}"
