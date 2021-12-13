from django.db import models


class Employee(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title
