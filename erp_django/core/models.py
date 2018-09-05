from django.db import models

PROJECT_TYPE_VARIATIONS = (
        ("OUTSTAFF", "outstaff"),
        ("FIX_PRICE_PROJECT", "fix price project"),
        ("TIME_AND_MATERIAL", "time & material")
    )


class GeneralInfo(models.Model):
    manager_name = models.CharField(max_length=50)
    manager_surname = models.CharField(max_length=100)
    address = models.TextField()
    bank_requisites = models.TextField()

    def __str__(self):
        return self.manager_surname


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    client_address = models.TextField()
    project_type = models.CharField(choices=PROJECT_TYPE_VARIATIONS, max_length=50)
    currency = models.CharField(max_length=20)
    basic_price = models.FloatField()
    general_info = models.ForeignKey(GeneralInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name


class Invoice(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    expected_payout_date = models.DateField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)


class Services(models.Model):
    price = models.FloatField()
    quantity = models.FloatField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return self.price * self.quantity
