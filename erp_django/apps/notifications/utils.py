import datetime

from django.db.models import Q

from apps.core.models import User, Vacation, Project, Developer
from apps.notifications.models import Notification


class NotificationsProcessor:

    def __init__(self):
        self.now = datetime.datetime.now()
        self.tomorrow = self.now + datetime.timedelta(days=1)
        self.next_week = self.now + datetime.timedelta(days=7)
        self.fields = {
            'user': None,
            'title': '',
            'description': '',
            'type_notice': ''
        }
        self.users_all = User.objects.all()

    def process(self):
        self.set_birthdays()
        self.set_vacations()
        self.set_projects_start()
        self.set_projects_deadline()

    def set_birthdays(self):
        notifications = []
        users_birthdays = User.objects.filter(Q(birthday_date=self.tomorrow) | Q(birthday_date=self.next_week))

        for user in self.users_all:
            for birthday in users_birthdays:
                if user is birthday:
                    continue

                self.fields['user'] = user
                self.fields['title'] = f"{birthday.first_name}'s birthday!"
                self.fields['description'] = f"{birthday.last_name} {birthday.first_name}'s birthday will be on " \
                    f"{birthday.birthday_date}"
                self.fields['type_notice'] = 'BIRTHDAY'

                notifications.append(Notification(**self.fields))
        Notification.objects.bulk_create(notifications)

    def set_vacations(self):
        notifications = []
        vacations = Vacation.objects.filter(Q(from_date=self.tomorrow) | Q(from_date=self.next_week))

        for user in self.users_all:
            for vacation in vacations:
                if user is vacations.user:
                    continue

                self.fields['user'] = user
                self.fields['title'] = f"{vacation.user.first_name}'s vacation!"
                self.fields['description'] = f"{vacation.user.last_name} {vacation.user.first_name}'s vacation starts " \
                    f"on {vacation.from_date}"
                self.fields['type_notice'] = 'VACATION'

                notifications.append(Notification(**self.fields))
        Notification.objects.bulk_create(notifications)

    def set_projects_start(self):
        notifications = []

        projects = Project.objects.filter(Q(from_date=self.tomorrow) | Q(from_date=self.next_week)).select_related(
            'manager_info', 'client')

        for project in projects:
            user_ids = []

            dev_id = list(Developer.objects.filter(project=project).values_list('id', flat=True))
            manager_id = project.manager_info.id
            client_id = project.client.id

            user_ids += dev_id
            user_ids.append(manager_id)
            user_ids.append(client_id)

            users = User.objects.filter(id__in=user_ids)

            for user in users:
                self.fields['user'] = user
                self.fields['title'] = f"Start of project {project.project_name}!"
                self.fields['description'] = f"Project {project.project_name} starts on {project.project_started_date}"
                self.fields['type_notice'] = 'START_PROJECT'

                notifications.append(Notification(**self.fields))
        Notification.objects.bulk_create(notifications)

    def set_projects_deadline(self):
        notifications = []

        projects = Project.objects.filter(Q(deadline=self.tomorrow) | Q(deadline=self.next_week)).select_related(
            'manager_info', 'client')

        for project in projects:
            user_ids = []

            dev_id = list(Developer.objects.filter(project=project).values_list('id', flat=True))
            manager_id = project.manager_info.id
            client_id = project.client.id

            user_ids += dev_id
            user_ids.append(manager_id)
            user_ids.append(client_id)

            users = User.objects.filter(id__in=user_ids)

            for user in users:
                self.fields['user'] = user
                self.fields['title'] = f"Deadline for project {project.project_name}!"
                self.fields[
                    'description'] = f"Deadline for project {project.project_name} will be on " \
                    f"{project.project_started_date}"
                self.fields['type_notice'] = 'DEADLINE'

                notifications.append(Notification(**self.fields))
        Notification.objects.bulk_create(notifications)
