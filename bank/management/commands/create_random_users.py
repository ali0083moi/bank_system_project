import random
from django.core.management.base import BaseCommand
from bank.models import User


class Command(BaseCommand):
    help = 'Create random users'

    def handle(self, *args, **kwargs):
        first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Hank']
        last_names = ['Smith', 'Doe', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez']

        users = []
        for _ in range(5000):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            id_number = ''.join(random.choices('0123456789', k=10))
            users.append(User(first_name=first_name, last_name=last_name, id_number=id_number))

        User.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS('Successfully created 5,000 random users'))
