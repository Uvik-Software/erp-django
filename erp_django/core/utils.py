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
import datetime
from datetime import timedelta


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


def get_orthodox_easter(year, method=2):
    """
    This method was ported from the work done by GM Arts,
    on top of the algorithm by Claus Tondering, which was
    based in part on the algorithm of Ouding (1940), as
    quoted in "Explanatory Supplement to the Astronomical
    Almanac", P.  Kenneth Seidelmann, editor.

    This algorithm implements three different easter
    calculation methods:

    1 - Original calculation in Julian calendar, valid in
        dates after 326 AD
    2 - Original method, with date converted to Gregorian
        calendar, valid in years 1583 to 4099
    3 - Revised method, in Gregorian calendar, valid in
        years 1583 to 4099 as well


    * ``EASTER_JULIAN   = 1``
    * ``EASTER_ORTHODOX = 2``
    * ``EASTER_WESTERN  = 3``

    The default method is method 2.

    More about the algorithm may be found at:

    `GM Arts: Easter Algorithms <http://www.gmarts.org/index.php?go=415>`_

    and

    `The Calendar FAQ: Easter <https://www.tondering.dk/claus/cal/easter.php>`_

    """

    if not (1 <= method <= 3):
        raise ValueError("invalid method")

    # g - Golden year - 1
    # c - Century
    # h - (23 - Epact) mod 30
    # i - Number of days from March 21 to Paschal Full Moon
    # j - Weekday for PFM (0=Sunday, etc)
    # p - Number of days from March 21 to Sunday on or before PFM
    #     (-6 to 28 methods 1 & 3, to 56 for method 2)
    # e - Extra days to add for method 2 (converting Julian
    #     date to Gregorian date)

    y = year
    g = y % 19
    e = 0
    if method < 3:
        # Old method
        i = (19 * g + 15) % 30
        j = (y + y // 4 + i) % 7
        if method == 2:
            # Extra dates to convert Julian to Gregorian date
            e = 10
            if y > 1600:
                e = e + y // 100 - 16 - (y // 100 - 16) // 4
    else:
        # New method
        c = y // 100
        h = (c - c // 4 - (8 * c + 13) // 25 + 19 * g + 15) % 30
        i = h - (h // 28) * (1 - (h // 28) * (29 // (h + 1)) * ((21 - g) // 11))
        j = (y + y // 4 + i + 2 - c + c // 4) % 7

    # p can be from -6 to 56 corresponding to dates 22 March to 23 May
    # (later dates apply to method 2, although 23 May never actually occurs)
    p = i - j + e
    d = 1 + (p + 27 + (p + 6) // 40) % 31
    m = 3 + (p + 26) // 30
    return datetime.date(int(y), int(m), int(d))


def get_troica_date(easter_date):
    return easter_date + timedelta(days=49)


def get_ua_days_off(next_month_only=True):
    current_date = datetime.date.today()
    easter = get_orthodox_easter(current_date.year)
    troica = get_troica_date(easter)
    days_off = {"new_year": datetime.date(current_date.year, 1, 1),
                "orthodox_xmas": datetime.date(current_date.year, 1, 7),
                "catholic_xmas": datetime.date(current_date.year, 12, 25),
                "women_day": datetime.date(current_date.year, 3, 8),
                "labour_day": datetime.date(current_date.year, 5, 1),
                "victory_day": datetime.date(current_date.year, 5, 9),
                "constitution_day": datetime.date(current_date.year, 6, 28),
                "independence_day": datetime.date(current_date.year, 8, 24),
                "day_of_ukrainian_army": datetime.date(current_date.year, 10, 14),
                "easter": easter,
                "troica": troica}
    if next_month_only:
        till_date = current_date + timedelta(days=30)
        next_month_holidays = dict()
        for day in days_off:
            if till_date >= days_off[day] >= current_date:
                next_month_holidays[day] = days_off[day]
        return next_month_holidays
    return days_off
