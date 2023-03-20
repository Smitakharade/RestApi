from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=200)
    salary = models.FloatField()
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = "Employee"

    @staticmethod
    def avgsal():
        pass

    def show_details(self):
        print(f"Name: {self.name}\nSalary:{self.salary}\nDate_joined: {self.date_joined}\nis_active:{self.is_active}")
