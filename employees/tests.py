from django.http import response
from django.test import TestCase
from faker import Faker
from employees.models import Employee

class TestPagination(TestCase):

    def setUp(self):
        faker = Faker()

        for _ in range (102):
            Employee.objects.create(title=faker.job())
    
    def test_index_view(self):
        response_1 = self.client.get('/employees/')
        response_2 = self.client.get('/employees/?page=1')
        self.assertEqual(response_1.content, response_2.content)

        
        
       
        




