INVOICE_REQUIRED_FIELDS = {"invoice_date", "due_date", "project_id", "download", "owner"}

ACT_JOBS_REQUIRED_FIELDS = {"act_jobs_date", "act_jobs_numb", "developer_id", "download"}

NOTIFICATION_TYPES = (
    ("UNPAID_INVOICE", "unpaid invoice"),
    ("BIRTHDAY", "birthday"),
    ("DEADLINE", "deadline")
)

GMAIL_EMAIL = "dmitry.ko@uvik.net"
GMAIL_PASSWORD = "uDEFpm74!!"

G_CALENDAR_ID = "semmy071997@gmail.com"
G_API_KEY = "AIzaSyAP6cEUZ0ngz7pNgk8RDGLjuiDpe87BsqI"

# VARS FOR NOTIFICATIONS
NUMBER_OF_DAYS_FOR_OUTDATED_INVOICE = 15
NUMBER_OF_DAYS_FOR_BIRTHDAY_NOTIFICATION = 7
NUMBER_OF_DAYS_FOR_DEADLINE_NOTIFICATION = 14
