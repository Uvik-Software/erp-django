from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Developer, Project, Vacation, Manager, DeadlineForGCal, ProjectStartForGCal
from core.utils import create_g_calendar_event, gmail_sender, update_g_calendar_event
from django.conf import settings
from rest_framework.authtoken.models import Token


def disconnect_signal(signal, receiver, sender):
    disconnect = getattr(signal, 'disconnect')
    disconnect(receiver, sender)


def reconnect_signal(signal, receiver, sender):
    connect = getattr(signal, 'connect')
    connect(receiver, sender=sender)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Developer)
def add_birthday_to_google_calendar(sender, instance, created, update_fields, **kwargs):
    if created:
        dev = instance
        message = "%s has a birthday today" % dev.first_name + ' ' + dev.last_name
        # uncomment to create an actual event in google calendar
        # create_g_calendar_event(dev.birthday_date, dev.birthday_date, message)


@receiver(post_save, sender=Project)
def add_project_deadline_google_calendar(sender, instance, created, update_fields, **kwargs):
    if created:
        project = instance
        if project.deadline:
            msg = "Deadline for project '%s'" % project.project_name
            # uncomment to create an actual event in google calendar
            event_id = create_g_calendar_event(project.deadline, project.deadline, msg)
            deadline_object = DeadlineForGCal.objects.create(project=project, event_id=event_id)


@receiver(pre_save, sender=Project)
def change_project_deadline_google_calendar(sender, instance, update_fields, **kwargs):
    try:
        old_proj_inst = Project.objects.get(id=instance.id)
    except Project.DoesNotExist:
        pass
    else:
        project = instance
        if project.deadline != old_proj_inst.deadline:
            email_managers = [email_man.email for email_man in
                              Manager.objects.exclude(email=project.manager_info.email).all()]
            msg = "Deadline for project '%s' has changed" % project.project_name
            sbj = "Changes for project '%s' deadline" % project.project_name
            gmail_sender(msg, project.manager_info.email, sbj, cc=email_managers)
            # uncomment to update an actual event in google calendar
            event_id = project.deadlineforgcal.event_id
            update_event_id = update_g_calendar_event(project.deadline, project.deadline, msg, event_id)
            project.deadlineforgcal.event_id = update_event_id
            project.deadlineforgcal.save()


@receiver(post_save, sender=Project)
def add_project_started_date_google_calendar(sender, instance, created, update_fields, **kwargs):
    if created:
        project = instance
        if project.project_started_date:
            msg = "Project '%s' is started" % project.project_name
            # uncomment to create an actual event in google calendar
            event_id = create_g_calendar_event(project.project_started_date, project.project_started_date, msg)
            project_start_object = ProjectStartForGCal.objects.create(project=project, event_id=event_id)


@receiver(pre_save, sender=Project)
def change_project_started_date_google_calendar(sender, instance, update_fields, **kwargs):
    try:
        old_proj_inst = Project.objects.get(id=instance.id)
    except Project.DoesNotExist:
        pass
    else:
        project = instance
        if project.project_started_date != old_proj_inst.project_started_date:
            email_managers = [email_man.email for email_man in
                              Manager.objects.exclude(email=project.manager_info.email).all()]
            msg = "Project started date for project '%s' has changed" % project.project_name
            sbj = "Changes for project '%s' started date" % project.project_name
            gmail_sender(msg, project.manager_info.email, sbj, cc=email_managers)
            # uncomment to update an actual event in google calendar
            event_id = project.projectstartforgcal.event_id
            update_event_id = update_g_calendar_event(project.project_started_date, project.project_started_date,
                                                      msg, event_id)
            project.projectstartforgcal.event_id = update_event_id
            project.projectstartforgcal.save()


@receiver(pre_save, sender=Vacation)
def notify_dev_if_vacation_approved(sender, instance, update_fields, **kwargs):
    try:
        old_vac_inst = Vacation.objects.get(id=instance.id)
    except Vacation.DoesNotExist:
        pass
    else:
        vacation = instance
        if vacation.approved != old_vac_inst.approved:
            sbj = "Approvement about your vacation is left"
            msg = "Approvement about your vacation is updated"
            # uncomment to send a real email
            gmail_sender(msg, vacation.developer.email, sbj)
