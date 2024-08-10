import random
from django.core.management.base import BaseCommand
from bank.models import BankAccount, User
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create 10 million random bank accounts'

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())
        accounts = []

        for _ in range(10000000):
            user = random.choice(users)
            account_number = ''.join(random.choices('0123456789', k=16))
            balance = Decimal(random.uniform(0, 10000000)).quantize(Decimal('0.01'))
            accounts.append(BankAccount(owner=user, account_number=account_number, balance=balance))

            if len(accounts) % 10000 == 0:
                BankAccount.objects.bulk_create(accounts)
                accounts = []

        if accounts:
            BankAccount.objects.bulk_create(accounts)

        self.stdout.write(self.style.SUCCESS('Successfully created 10 million bank accounts'))
