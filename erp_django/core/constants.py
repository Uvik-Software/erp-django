INVOICE_REQUIRED_FIELDS = set(["invoice_date", "due_date", "project_id", "download"])

PROJECT_TYPE_VARIATIONS = (
        ("OUTSTAFF", "outstaff"),
        ("FIX_PRICE_PROJECT", "fix price project"),
        ("TIME_AND_MATERIAL", "time & material")
    )

INVOICE_STATUS = (
    ("SENT", "sent"),
    ("WAITING_FOR_PAYMENT", "waiting for payment"),
    ("PAID", "paid")
)

NOTIFICATION_TYPES = (
    ("UNPAID_INVOICE", "unpaid invoice"),
    ("BIRTHDAY", "birthday"),
    ("DEADLINE", "deadline")
)

GMAIL_EMAIL = "dmitry.ko@uvik.net"
GMAIL_PASSWORD = "uDEFpm74!!"

G_CALENDAR_ID = "uvik.net_l0ns61ouq9va8surjs4f690fik@group.calendar.google.com"

# VARS FOR NOTIFICATIONS
NUMBER_OF_DAYS_FOR_OUTDATED_INVOICE = 15
NUMBER_OF_DAYS_FOR_BIRTHDAY_NOTIFICATION = 7
NUMBER_OF_DAYS_FOR_DEADLINE_NOTIFICATION = 14
