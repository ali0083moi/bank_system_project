from decimal import Decimal

from django.db import transaction, models
from django.db.models import IntegerField, F, DecimalField, Sum
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from bank.models import BankAccount, User


def account_list(request):
    accounts = BankAccount.objects.all().values('owner__first_name', 'owner__last_name', 'balance')
    context = {
        'accounts': accounts
    }
    return render(request, 'account_list.html', context)


def max_balance(request):
    max_balance_account = BankAccount.objects.order_by('-balance').first()
    context = {
        'account': max_balance_account
    }
    return render(request, 'max_account.html', context)


def min_balances(request):
    accounts = BankAccount.objects.all().order_by('balance')[:5].values('owner__first_name', 'owner__last_name',
                                                                        'balance')
    context = {
        'accounts': accounts
    }
    return render(request, 'account_list.html', context)


@transaction.atomic
def transfer_funds(request):
    if request.method == 'POST':
        account_from_number = request.POST.get('account_from')
        account_to_number = request.POST.get('account_to')
        amount = Decimal(request.POST.get('amount'))

        try:
            account_from = BankAccount.objects.get(account_number=account_from_number)
        except BankAccount.DoesNotExist:
            return HttpResponse(f"Error: Account with number {account_from_number} does not exist.")

        try:
            account_to = BankAccount.objects.get(account_number=account_to_number)
        except BankAccount.DoesNotExist:
            return HttpResponse(f"Error: Account with number {account_to_number} does not exist.")

        if account_from.balance >= amount:
            account_from.balance -= amount
            account_to.balance += amount
            account_from.save()
            account_to.save()
            return HttpResponse(f"Successfully transferred {amount} from {account_from_number} to {account_to_number}")
        else:
            return HttpResponse("Error: Insufficient funds.")

    return render(request, 'transfer_funds.html')


def account_number_greater_balance(request):
    accounts = BankAccount.objects.annotate(
        id_as_decimal=Cast('account_number', DecimalField(max_digits=20, decimal_places=0))
    ).filter(
        id_as_decimal__gt=F('balance')
    ).values('owner__first_name', 'owner__last_name', 'balance')
    context = {
        'accounts': accounts
    }
    return render(request, 'account_list.html', context)


def id_greater_balance(request):
    accounts = BankAccount.objects.annotate(
        id_as_decimal=Cast('owner__id_number', DecimalField(max_digits=20, decimal_places=0))
    ).filter(
        id_as_decimal__gt=F('balance')
    ).values('owner__first_name', 'owner__last_name', 'balance')
    context = {
        'accounts': accounts
    }
    return render(request, 'account_list.html', context)


def get_total_balance_of_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id_number=user_id)
        except User.DoesNotExist:
            return HttpResponse(f"Error: User with ID {user_id} does not exist.")

        user_balance = user.bank_accounts.aggregate(total_balance=Sum('balance'))['total_balance']
        return HttpResponse(f"Total balance of {user.first_name} {user.last_name} is {user_balance}")

    return render(request, 'user_total_balance.html')
