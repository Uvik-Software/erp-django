from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from .models import DevelopersOnProject, Developer, Project, Company
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .constants import GMAIL_EMAIL, GMAIL_PASSWORD, G_CALENDAR_ID
from calendar_api.calendar_api import google_calendar_api
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


def gmail_html_sender(html_msg, email_destination):
    yag = yagmail.SMTP(GMAIL_EMAIL, GMAIL_PASSWORD)
    yag.send(email_destination, "Invoice", html_msg)


def create_g_calendar_event(start_date, end_date, description):
    m = google_calendar_api()
    m.create_event(calendar_id=G_CALENDAR_ID,
                   start=start_date,
                   end=end_date,
                   desc=description)
