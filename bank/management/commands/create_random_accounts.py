import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from bank.models import User, BankAccount


class Command(BaseCommand):
    help = 'Create random bank accounts'

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())

        def create_random_accounts(n):
            accounts = []
            for _ in range(n):
                user = random.choice(users)
                account_number = ''.join(random.choices('0123456789', k=16))
                balance = Decimal(random.uniform(0, 10000000)).quantize(Decimal('0.01'))
                accounts.append(BankAccount(owner=user, account_number=account_number, balance=balance))
            return accounts

        with transaction.atomic():
            BankAccount.objects.bulk_create(create_random_accounts(20000))

        self.stdout.write(self.style.SUCCESS('Successfully created 20,000 random bank accounts'))
