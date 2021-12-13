from faker import Faker
from django.core.management.base import BaseCommand

from employees.models import Employee

class Command(BaseCommand):

    def handle(self, *args, **options):
        faker = Faker()

        for _ in range (102):
            Employee.objects.create(title=faker.job())
