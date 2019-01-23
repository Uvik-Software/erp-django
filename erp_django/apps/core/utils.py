
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template

from django.http import JsonResponse
from .constants import GMAIL_EMAIL, GMAIL_PASSWORD, G_CALENDAR_ID
from calendar_api.calendar_api import google_calendar_api

import yagmail
import datetime
from datetime import timedelta


def generate_pdf_from_html(template_file, data):
    template = get_template(template_file)
    html = template.render(data)
    pdf_response = BytesIO()
    encoded_html = BytesIO(html.encode("UTF-8"))
    pdf = pisa.pisaDocument(encoded_html, pdf_response, encoding='utf-8')
    # pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), pdf_response, encoding='UTF-8')
    return pdf_response, html


def pdf_to_google_drive(html):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file1 = drive.CreateFile(
        {'title': 'Hello.pdf', 'mimeType': 'application/pdf'})
    file1.SetContentString(html)
    file1.Upload()


def gmail_sender(msg, email_destination, subject, cc=None):
    yag = yagmail.SMTP(GMAIL_EMAIL, GMAIL_PASSWORD)
    if isinstance(email_destination, list):
        for email in email_destination:
            yag.send(email, subject, msg)
    else:
        yag.send(email_destination, subject, msg, cc=cc)


def create_g_calendar_event(start_date, end_date, description):
    m = google_calendar_api()
    return m.create_event(calendar_id=G_CALENDAR_ID,
                          start=str(start_date) + "T00:00:00-00:00",
                          end=str(end_date) + "T00:00:00-00:00",
                          desc=description)


def update_g_calendar_event(start_date, end_date, description, event_id):
    g_cal = google_calendar_api()
    return g_cal.update_event(calendar_id=G_CALENDAR_ID,
                              event_id=event_id,
                              start=start_date,
                              end=end_date,
                              desc=description)


def is_manager(user):
    return user.type == "MANAGER"


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
    if next_month_only is True:
        till_date = current_date + timedelta(days=30)
        next_month_holidays = dict()
        for day in days_off:
            if till_date >= days_off[day] >= current_date:
                next_month_holidays[day] = days_off[day]
        return next_month_holidays
    return days_off


def json_response_error(message=None):
    return JsonResponse({"ok": False,
                         "message": message})


def json_response_success(message=None, data=None, status=200):
    if data is None:
        data = dict()
    if message is None:
        message = ""
    return JsonResponse({"ok": True,
                         "message": message,
                         "data": data}, status=status)


def is_developer(user):
    return user.type == "DEVELOPER"


def check_empty_fields(seq):
    seq_check = []
    is_filled = True
    empty = False

    for item in seq:
        if item:
            seq_check.append(is_filled)
        else:
            seq_check.append(empty)

    if False in seq_check:
        return False

    return True

