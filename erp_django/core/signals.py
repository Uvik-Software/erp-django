from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Developer, Project, Vacation
from .utils import create_g_calendar_event, gmail_sender


def disconnect_signal(signal, receiver, sender):
    disconnect = getattr(signal, 'disconnect')
    disconnect(receiver, sender)


def reconnect_signal(signal, receiver, sender):
    connect = getattr(signal, 'connect')
    connect(receiver, sender=sender)


@receiver(post_save, sender=Developer)
def add_birthday_to_google_calendar(sender, instance, created, update_fields, **kwargs):
    if created:
        dev = instance
        message = "%s has a birthday today" % dev.name + dev.surname
        create_g_calendar_event(dev.birthday_date, dev.birthday_date, message)


@receiver(post_save, sender=Project)
def add_project_deadline_google_calendar(sender, instance, created, update_fields, **kwargs):

    # TODO: check if deadline is changed, not just set. and if True, then remove previous google event and add a new one
    # Links that will help:
    # https://bitbucket.org/kingmray/django-google-calendar/src/3856538e28822c5ffaba39a3258a9e833ffe413a/calendar_api/calendar_api.py?at=master&fileviewer=file-view-default
    # https://stackoverflow.com/questions/36719566/identify-the-changed-fields-in-django-post-save-signal

    project = instance
    if project.deadline:
        message = "Deadline for project '%s'" % project.project_name
        # uncomment to create an actual event in google calendar
        #create_g_calendar_event(project.deadline, project.deadline, message)
        print(message)


@receiver(post_save, sender=Project)
def add_project_started_date_google_calendar(sender, instance, created, update_fields, **kwargs):

    # TODO: also check if this field is changed. same as for deadline

    project = instance
    if project.project_started_date:
        message = "project '%s' is started" % project.project_name
        # uncomment to create an actual event in google calendar
        #create_g_calendar_event(project.project_started_date, project.project_started_date, message)
        print(message)


@receiver(post_save, sender=Vacation)
def notify_dev_if_comment_is_left(sender, instance, created, update_fields, **kwargs):

    # TODO: also check if this field is changed. same as for deadline

    vacation = instance
    if vacation.comments:
        sbj = "Comment regarding vacation is left"
        msg = "Comment about your vacation is updated"
        # uncomment to send a real email
        # gmail_sender(msg, vacation.developer.email, sbj)
        print(msg)
