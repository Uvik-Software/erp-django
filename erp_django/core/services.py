from core.models import DevelopersOnProject, Developer, Project, Company, SentNotifications, Invoice, Manager, \
    InvoiceNotifications, BirthdayNotification, DeadlineNotifications
from django.core.exceptions import ObjectDoesNotExist

from .constants import NUMBER_OF_DAYS_FOR_BIRTHDAY_NOTIFICATION, NUMBER_OF_DAYS_FOR_DEADLINE_NOTIFICATION, \
    NUMBER_OF_DAYS_FOR_OUTDATED_INVOICE

from datetime import date

from django.http import JsonResponse

from .utils import gmail_sender


def get_project_developers_and_cost(project):
    developers_on_project = [dev for dev in DevelopersOnProject.objects.filter(project=project)]
    developers = list()
    total_cost = 0 if not project.basic_price else project.basic_price
    for developer in developers_on_project:
        dev_info = Developer.objects.get(id=developer.developer_id)
        cost = dev_info.hourly_rate * developer.hours
        dev = dict(id=developer.id,
                   worked_hours=developer.hours,
                   description=developer.description,
                   hourly_rate=dev_info.hourly_rate,
                   cost=cost)
        if not project.basic_price:
            total_cost += cost
        developers.append(dev)

    return developers, total_cost


def get_project_details(project_id):
    try:
        project = Project.objects.get(id=project_id)
    except ObjectDoesNotExist:
        return JsonResponse({"status": "No such project"})
    else:
        return project


def get_company_details_by_currency(currency):
    try:
        company_details = Company.objects.get(currency=currency)
    except ObjectDoesNotExist:
        return JsonResponse({"status": "Please provide '%s' details for the company" % currency})
    else:
        return company_details


def outdated_invoice_checker(invoices):
    for invoice in invoices:
        date_dif = date.today() - invoice.date
        if date_dif.days == NUMBER_OF_DAYS_FOR_OUTDATED_INVOICE and \
                not InvoiceNotifications.objects.filter(event_id=invoice.id):
            subject = "Unpaid Invoice"
            msg = "Invoice with ID %s is unpaid for more than 15 days" % invoice.id
            to_email = invoice.project_id.general_info.manager_email
            InvoiceNotifications.objects.create(notification_type="UNPAID_INVOICE",
                                                event_id=invoice.id).save()
            gmail_sender(msg, to_email, subject)


def project_deadline_checker(projects):
    for project in projects:
        date_dif = date.today() - project.deadline
        if date_dif.days == NUMBER_OF_DAYS_FOR_DEADLINE_NOTIFICATION and \
                not DeadlineNotifications.objects.filter(event_id=project.id):
            subject = "Deadline for the project '%s'" % project.project_name
            msg = "Deadline for the project '%s' will be %s " % (project.project_name, project.deadline)
            to_email = project.general_info.manager_email
            DeadlineNotifications.objects.create(notification_type="DEADLINE",
                                                 event_id=project.id).save()
            gmail_sender(msg, to_email, subject)


def dev_birthday_checker(devs):
    for dev in devs:
        date_dif = date.today() - dev.birthday_date
        if date_dif.days == NUMBER_OF_DAYS_FOR_BIRTHDAY_NOTIFICATION and \
                not BirthdayNotification.objects.filter(event_id=dev.id):
            subject = "Birthday notification"
            msg = "%s will have a birthday soon" % dev.name + dev.surname
            dev_emails = [dev.email for dev in devs]
            managers_emails = [manager.email for manager in Manager.objects.all()]
            to_email = dev_emails + managers_emails
            BirthdayNotification.objects.create(notification_type="BIRTHDAY",
                                                event_id=dev.id).save()
            gmail_sender(msg, to_email, subject)


def get_developer_bank_data(developer):
    dev_bank = developer.bank_info
    info = []
    dev_b_in = dict(bank_name=dev_bank.bank_name,
                    bank_account_number=dev_bank.bank_account_number,
                    bank_code=dev_bank.bank_code)
    info.append(dev_b_in)
    return info


def get_owner_bank_data(owner):
    owner_bank = owner.bank_info
    info = []
    owner_b_in = dict(bank_name=owner_bank.bank_name,
                      bank_account_number=owner_bank.bank_account_number,
                      bank_code=owner_bank.bank_code)
    info.append(owner_b_in)
    return info
