from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from .models import DevelopersOnProject, Developer, Project, Company, SentNotifications, Invoice, ManagerInfo, \
    InvoiceNotifications, BirthdayNotification, DeadlineNotifications
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .constants import GMAIL_EMAIL, GMAIL_PASSWORD, G_CALENDAR_ID, NUMBER_OF_DAYS_FOR_BIRTHDAY_NOTIFICATION, \
    NUMBER_OF_DAYS_FOR_DEADLINE_NOTIFICATION, NUMBER_OF_DAYS_FOR_OUTDATED_INVOICE
from calendar_api.calendar_api import google_calendar_api
from datetime import date
import yagmail


def generate_pdf_from_html(template_file, data):
    template = get_template(template_file)
    html = template.render(data)
    pdf_response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf_response)
    return pdf_response, html


def pdf_to_google_drive(html):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile(
        {'title': 'Hello.pdf', 'mimeType': 'application/pdf'})
    file1.SetContentString(html)
    file1.Upload()


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


def gmail_sender(msg, email_destination, subject):
    yag = yagmail.SMTP(GMAIL_EMAIL, GMAIL_PASSWORD)
    if isinstance(email_destination, list):
        for email in email_destination:
            yag.send(email, subject, msg)
    else:
        yag.send(email_destination, subject, msg)


def create_g_calendar_event(start_date, end_date, description):
    m = google_calendar_api()
    m.create_event(calendar_id=G_CALENDAR_ID,
                   start=start_date,
                   end=end_date,
                   desc=description)


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
            managers_emails = [manager.manager_email for manager in ManagerInfo.objects.all()]
            to_email = dev_emails + managers_emails
            BirthdayNotification.objects.create(notification_type="BIRTHDAY",
                                                event_id=dev.id).save()
            gmail_sender(msg, to_email, subject)


def is_manager(user):
    return user.groups.filter(name='managers').exists()
