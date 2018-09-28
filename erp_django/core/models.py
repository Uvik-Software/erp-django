from django.db import models
from .constants import PROJECT_TYPE_VARIATIONS, INVOICE_STATUS, NOTIFICATION_TYPES
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    user_type = models.CharField(choices=(
        ("MANAGER", "manager"),
        ("DEVELOPER", "developer"),
        ("CLIENT", "client"),
        ("JUST_CREATED", "just created")
    ), max_length=30, default="JUST_CREATED")

# TODO: do normalization


class ManagerInfo(models.Model):
    manager_name = models.CharField(max_length=50)
    manager_surname = models.CharField(max_length=100)
    manager_email = models.EmailField()
    manager_position = models.CharField(max_length=50)
    address = models.TextField()
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.manager_email


class Client(models.Model):
    name = models.CharField(max_length=35)
    position = models.CharField(max_length=100)
    company_name = models.CharField(max_length=300)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    identification_number = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class Developer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    hourly_rate = models.IntegerField()
    birthday_date = models.DateField()
    monthly_salary = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_type = models.CharField(choices=PROJECT_TYPE_VARIATIONS, max_length=50)
    project_description = models.TextField()
    currency = models.CharField(max_length=20)
    basic_price = models.FloatField(null=True)
    general_info = models.ForeignKey(ManagerInfo, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    all_time_money_spent = models.IntegerField()
    deadline = models.DateField(null=True)
    project_started_date = models.DateField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name


class DevelopersOnProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    description = models.TextField()
    hours = models.FloatField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Invoice(models.Model):
    date = models.DateField()
    expected_payout_date = models.DateField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(choices=INVOICE_STATUS, max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project_id)


class Company(models.Model):
    currency = models.CharField(max_length=3)
    bank_account_number = models.IntegerField()
    beneficiary = models.CharField(max_length=50)
    iban = models.CharField(max_length=50)
    swift = models.CharField(max_length=50)
    bank_address = models.TextField()
    sign = models.ImageField(upload_to='static/signs/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class DevSalary(models.Model):
    date = models.IntegerField(default=12,
                               validators=[MaxValueValidator(31), MinValueValidator(1)])
    comment = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class SentNotifications(models.Model):
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.notification_type


class InvoiceNotifications(SentNotifications):
    event_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)


class BirthdayNotification(SentNotifications):
    event_id = models.ForeignKey(Developer, on_delete=models.CASCADE)


class DeadlineNotifications(SentNotifications):
    event_id = models.ForeignKey(Project, on_delete=models.CASCADE)


class Cv(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    g_drive_link = models.URLField()

    def __str__(self):
        return self.g_drive_link
