from django.db import models
from datetime import date

class Contact(models.Model):
    phone = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.phone


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Compensation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    contact = models.OneToOneField(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    compensations = models.ManyToManyField(Compensation)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Job(models.Model):
    title = models.CharField(max_length=255)
    employees = models.ManyToManyField(Employee, through='Assignment')

    def __str__(self):
        return self.title


class Assignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.ForeignKey(Job, on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField(default=date(9999, 12, 31))