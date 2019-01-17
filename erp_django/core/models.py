from django.db import models
from .constants import PROJECT_TYPE_VARIATIONS, INVOICE_STATUS, NOTIFICATION_TYPES
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# from core.utils import gmail_sender


class User(AbstractUser):
    USER_TYPES = (
        ("MANAGER", "Manager"),
        ("DEVELOPER", "Developer"),
        ("CLIENT", "Client"),
        ("JUST_CREATED", "Just created")
    )

    type = models.CharField(choices=USER_TYPES, max_length=30, default="JUST_CREATED")
    address = models.TextField(default='', blank=True)
    position = models.CharField(max_length=128, default='', blank=True)
    birthday_date = models.DateField(null=True)
    tax_number = models.CharField(max_length=20, default='')


# TODO: do normalization


class Manager(User):
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Manager {self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Manager'


class BankInfo(models.Model):
    bank_name = models.CharField(max_length=20, null=True)
    bank_account_number = models.CharField(max_length=50, null=True)
    bank_address = models.TextField(null=True)
    bank_code = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.bank_name


# rename to Customer ?
class Owner(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=50, null=True)
    father_name = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    tax_number = models.CharField(max_length=20, null=True)
    num_contract_with_dev = models.CharField(max_length=20, null=True)
    date_contract_with_dev = models.DateField(null=True)
    sign = models.ImageField(upload_to='static/signs/', null=True)
    bank_info = models.OneToOneField(BankInfo, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Owner {self.last_name} {self.first_name}"


class Client(User):
    company_name = models.CharField(max_length=300)
    phone = models.CharField(max_length=50)
    identification_number = models.CharField(max_length=32, default='')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"Client {self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Client'


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_type = models.CharField(choices=PROJECT_TYPE_VARIATIONS, max_length=50)
    project_description = models.TextField()
    currency = models.CharField(max_length=20)
    basic_price = models.FloatField(null=True)
    manager_info = models.ForeignKey(Manager, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    all_time_money_spent = models.IntegerField(default=0)
    deadline = models.DateField(null=True)
    project_started_date = models.DateField(null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    # __original_deadline = None
    # __original_project_started_date = None
    #
    # def __init__(self, *args, **kwargs):
    #     super(Project, self).__init__(*args, **kwargs)
    #     self.__original_deadline = self.deadline
    #     self.__original_project_started_date = self.project_started_date
    #
    # def save(self, force_insert=False, force_update=False, *args, **kwargs):
    #     if self.project_started_date != self.__original_project_started_date:
    #         email_managers = [email_man.email for email_man in
    #                           Manager.objects.exclude(email=self.manager_info.email).all()]
    #         sbj = "Changes in project started date"
    #         msg = "Project started date has changed"
    #         # uncomment to send a real email
    #         gmail_sender(msg, self.manager_info.email, sbj, cc=email_managers)
    #     if self.deadline != self.__original_deadline:
    #         email_managers = [email_man.email for email_man in
    #                           Manager.objects.exclude(email=self.manager_info.email).all()]
    #         sbj = "Changes in project deadline"
    #         msg = "Project deadline has changed"
    #         # uncomment to send a real email
    #         gmail_sender(msg, self.manager_info.email, sbj, cc=email_managers)
    #
    #     super(Project, self).save(force_insert, force_update, *args, **kwargs)
    #     self.__original_deadline = self.deadline
    #     self.__original_project_started_date = self.project_started_date

    def __str__(self):
        return self.project_name


class Developer(User):
    father_name = models.CharField(max_length=20, default='', blank=True)
    hourly_rate = models.IntegerField()
    monthly_salary = models.IntegerField()
    sign = models.ImageField(upload_to='static/signs/', null=True)
    bank_info = models.OneToOneField(BankInfo, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Developer {self.last_name} {self.first_name}, {self.email}"

    class Meta:
        verbose_name = 'Developer'


class DevelopersOnProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    hours = models.FloatField(null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


class Invoice(models.Model):
    date = models.DateField()
    expected_payout_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(choices=INVOICE_STATUS, max_length=50)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project)


class ActOfPerfJobs(models.Model):
    date = models.DateField()
    number_of_act = models.CharField(max_length=20)
    # owner_info = models.ForeignKey(Owner, on_delete=models.CASCADE)
    developer_info = models.ForeignKey(Developer, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE)


# What about this??
class Company(models.Model):
    currency = models.CharField(max_length=3)
    bank_account_number = models.IntegerField()
    beneficiary = models.CharField(max_length=50)
    iban = models.CharField(max_length=50)
    swift = models.CharField(max_length=50)
    bank_address = models.TextField()
    sign = models.ImageField(upload_to='static/signs/')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = "Company Currency"
        verbose_name_plural = "Company Currency"


class Vacation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    comments = models.TextField(default='', blank=True)
    approved = models.BooleanField(default=False)

    # __original_approved = None
    #
    # def __init__(self, *args, **kwargs):
    #     super(Vacation, self).__init__(*args, **kwargs)
    #     self.__original_approved = self.approved
    #
    # def save(self, force_insert=False, force_update=False, *args, **kwargs):
    #     if self.approved != self.__original_approved:
    #         sbj = "Approvement about your vacation is left"
    #         msg = "Approvement about your vacation is updated"
    #         # uncomment to send a real email
    #         gmail_sender(msg, self.developer.email, sbj)
    #
    #     super(Vacation, self).save(force_insert, force_update, *args, **kwargs)
    #     self.__original_approved = self.approved

    def __str__(self):
        return "Vacation {0}".format(self.id)


class DevSalary(models.Model):
    date = models.IntegerField(default=12,
                               validators=[MaxValueValidator(31), MinValueValidator(1)])
    comment = models.TextField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


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


class DeadlineForGCal(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=150)


class ProjectStartForGCal(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=150)
