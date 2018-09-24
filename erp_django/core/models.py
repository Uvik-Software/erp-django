from django.db import models
from .constants import PROJECT_TYPE_VARIATIONS, INVOICE_STATUS


class GeneralInfo(models.Model):
    manager_name = models.CharField(max_length=50)
    manager_surname = models.CharField(max_length=100)
    manager_email = models.EmailField()
    manager_position = models.CharField(max_length=50)
    address = models.TextField()
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.manager_surname


class Client(models.Model):
    name = models.CharField(max_length=35)
    position = models.CharField(max_length=100)
    company_name = models.CharField(max_length=300)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    identification_number = models.IntegerField()

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    hourly_rate = models.IntegerField()
    birthday_date = models.DateField()
    monthly_salary = models.IntegerField()

    def __str__(self):
        return self.email


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_type = models.CharField(choices=PROJECT_TYPE_VARIATIONS, max_length=50)
    project_description = models.TextField()
    currency = models.CharField(max_length=20)
    basic_price = models.FloatField(null=True)
    general_info = models.ForeignKey(GeneralInfo, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    all_time_money_spent = models.IntegerField()
    deadline = models.DateField(null=True)

    def __str__(self):
        return self.project_name


class DevelopersOnProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    description = models.TextField()
    hours = models.FloatField(null=True)


class Invoice(models.Model):
    date = models.DateField()
    expected_payout_date = models.DateField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(choices=INVOICE_STATUS, max_length=50)
    #spent_hours = models.FloatField(null=True)

    def __str__(self):
        return str(self.number)


class Services(models.Model):
    # not sure if we need this any more as now we are using Project and Developer for that purposes
    price = models.FloatField()
    quantity = models.FloatField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return self.price * self.quantity


class Company(models.Model):
    currency = models.CharField(max_length=3)
    bank_account_number = models.IntegerField()
    beneficiary = models.CharField(max_length=50)
    iban = models.CharField(max_length=50)
    swift = models.CharField(max_length=50)
    bank_address = models.TextField()
    sign = models.ImageField(upload_to='static/signs/')

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = "Company Currency"
        verbose_name_plural = "Company Currency"


class Vacation(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    comments = models.TextField(null=True)
    approved = models.BooleanField(default=False)


class DevSalary(models.Model):
    date = models.DateField()
    comment = models.TextField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
