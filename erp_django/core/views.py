from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework import viewsets, renderers, schemas, response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.schemas import AutoSchema

from .permissions import ManagerFullAccess, PermsForVacation

from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render

from .models import Invoice, Manager, Project, Developer, DevelopersOnProject, Client, Cv, Vacation, User, ActOfPerfJobs
from .serializers import InvoiceSerializer, ManagerSerializer, ProjectSerializer, \
    DeveloperSerializer, DevelopersOnProjectSerializer, ClientSerializer, UserSerializer, VacationSerializer, \
    ActOfPerfJobsSerializer

from .services import get_project_developers_and_cost, get_project_details, get_company_details_by_currency, \
    get_developer_bank_data, get_customer_bank_data

from .utils import pdf_to_google_drive, generate_pdf_from_html, is_manager, get_ua_days_off, \
    json_response_error, json_response_success, is_developer, gmail_sender

from .constants import INVOICE_REQUIRED_FIELDS, ACT_JOBS_REQUIRED_FIELDS
import json
import coreapi

from django.contrib.auth.hashers import make_password

# TODO: generate salary report for dev like we did for customer
# TODO: split views to files?


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((AllowAny,))
def schema_view(request):
    generator = schemas.SchemaGenerator(
        title='UVIK ERP API end points')
    return response.Response(generator.get_schema(request=request))


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user).data
    }


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (IsAuthenticated,)


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, ManagerFullAccess)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VacationViewSet(viewsets.ModelViewSet):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = (IsAuthenticated,)


class DevelopersOnProjectViewSet(viewsets.ModelViewSet):
    queryset = DevelopersOnProject.objects.all()
    serializer_class = DevelopersOnProjectSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)

    def get_queryset(self):
        project_id = self.request.GET.get('project_id', None)
        if project_id:
            return DevelopersOnProject.objects.all().filter(project_id=project_id)

        return DevelopersOnProject.objects.all()


class ActOfPerfJobsViewSet(viewsets.ModelViewSet):
    queryset = ActOfPerfJobs.objects.all()
    serializer_class = ActOfPerfJobsSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class DashboardReport(APIView):
    permission_classes = (IsAuthenticated, ManagerFullAccess)

    def get(self, request):
        developers = Developer.objects.all().count()
        clients = Client.objects.all().count()
        managers = Manager.objects.all().count()
        projects = Project.objects.all().count()
        return json_response_success(data=dict(number_of_developers=developers,
                                               number_of_managers=managers,
                                               number_of_clients=clients,
                                               number_of_projects=projects))


class GenerateInvoice(APIView):
    permission_classes = (IsAuthenticated, ManagerFullAccess)
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name="project_id",
                          type="integer",
                          required=True),
            coreapi.Field(name="invoice_date",
                          description='Invoice date in "YYYY-MM-DD" format.',
                          required=True),
            coreapi.Field(name="due_date",
                          required=True,
                          description='Due date in "YYYY-MM-DD" format.'),
            coreapi.Field(name="download",
                          type="boolean",
                          required=True)
        ]
    )

    def post(self, request):
        data = request.data
        if set(data.keys()) == INVOICE_REQUIRED_FIELDS:
            project_id = data["project_id"]
            invoice_date = data["invoice_date"]
            due_date = data["due_date"]
            download = data["download"]

            project = get_project_details(project_id)
            company_details = get_company_details_by_currency(project.currency)
            client_info = Client.objects.get(id=project.client.id)
            manager_info = Manager.objects.get(id=project.manager_info.id)
            developers, all_time_cost = get_project_developers_and_cost(project)
            total_cost = all_time_cost - project.all_time_money_spent

            # commented not to save projects and not to send files to google drive during dev.
            # should be uncommented later.

            #project.project.all_time_money_spent = total_cost
            #project.save()

            invoice = Invoice(date=invoice_date,
                              expected_payout_date=due_date,
                              project_id=project)
            #invoice.save()

            data = dict(developers_on_project=developers,
                        company_details=model_to_dict(company_details),
                        project=model_to_dict(project),
                        client_info=model_to_dict(client_info),
                        invoice=model_to_dict(invoice),
                        manager_info=model_to_dict(manager_info),
                        total_cost=total_cost)

            pdf_response, html = generate_pdf_from_html("invoices/invoice_2.html", data)
            #pdf_to_google_drive(html)
            #gmail_sender(html, client_info.email, "Invoice")

            if not download:
                data["company_details"]["sign"] = json.dumps(str(data["company_details"]["sign"]))
                return json_response_success(data=data)
            return HttpResponse(pdf_response.getvalue(), content_type='application/pdf')

        return json_response_error("Not all the required fields are filled up. %s are required."
                                   % INVOICE_REQUIRED_FIELDS)

    def get(self, request):
        """
            parameters:
            - name: invoice_id
              required: false
              type: int
        """
        data = request.query_params
        invoice_id = data.get("invoice_id", None)
        if not invoice_id:
            invoices = [invoice for invoice in Invoice.objects.all().values()]
            return json_response_success(data=invoices)

        invoice = get_object_or_404(Invoice, pk=invoice_id)
        return json_response_success(data=invoice)

    def delete(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice.delete()
        return json_response_success("Invoice deleted")


class DaysOff(APIView):
    permission_classes = (IsAuthenticated, ManagerFullAccess,)

    def get(self, request):
        """
            parameters:
            - name: next_month_only
              description: show only next month days off
              required: false
              type: bool
        """
        data = request.query_params
        next_month_only = data.get("next_month_only", True)

        next_month_days_off = get_ua_days_off(next_month_only)
        return json_response_success(data=next_month_days_off)

    def post(self, request):
        """
            parameters:
            - name: email
              description: client's email to whom we should send an email
              required: true
              type: string
        """
        email = request.data.get("email", None)
        if not email:
            return json_response_error("Should provide customer's email")

        next_month_days_off = get_ua_days_off()

        if not next_month_days_off:
            return json_response_success("No holidays in next 30 days")

        if next_month_days_off:
            # TODO: create html template and load info from it
            html = str(next_month_days_off)
            # uncomment to send a real email
            #gmail_sender(html, customer_email, "Ukrainian holidays")
            return json_response_success("Email to %s is succesfully sent" % email)


class DevelopersCv(APIView):
    permission_classes = (IsAuthenticated, ManagerFullAccess,)
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(name="name",
                          type="string",
                          required=False),
            coreapi.Field(name="surname",
                          type="string",
                          required=False),
        ]
    )

    def get(self, request):
        """
            parameters:
            - name: name
              description: Developer's name
              required: false
              type: string
            - name: surname
              description: Developer's surname
              required: false
              type: string
        """
        data = request.query_params

        if "name" in data:
            cv = [cv for cv in Cv.objects.filter(developer__name__contains=data["name"]).values()]
            return json_response_success(data=cv)
        if "surname" in data:
            cv = [cv for cv in Cv.objects.filter(developer__surname__contains=data["surname"]).values()]
            return json_response_success(data=cv)
        return json_response_success([cv for cv in Cv.objects.all().values()])

    def post(self, request):
        """
            parameters:
            - name: dev_id
              description: Developer's id
              required: true
              type: int
            - name: cv_link
              description: link to google drive where we have dev's resume
              required: true
              type: string
         """
        data = request.data
        dev_id = data.get("dev_id", None)
        cv_link = data.get("cv_link", None)

        if dev_id and cv_link:
            developer = get_object_or_404(Developer, pk=dev_id)
            cv = Cv(developer=developer,
                    g_drive_link=cv_link)
            cv.save()
            return json_response_success("CV created", model_to_dict(cv), status=201)
        return json_response_error("Not all the required fields are filled")

    def put(self, request):
        """
            parameters:
            - name: dev_id
              description: Developer's id
              required: true
              type: int
            - name: cv_link
              description: link to google drive where we have dev's resume
              required: true
              type: string
         """
        data = request.data
        dev_id = data.get("dev_id", None)
        cv_link = data.get("cv_link", None)
        data = request.query_params
        cv_id = data.get("id", None)

        if dev_id and cv_link:
            cv = get_object_or_404(Cv, id=cv_id)
            cv.g_drive_link = cv_link
            cv.save()
            return json_response_success("Link updated", model_to_dict(cv))
        return json_response_error("Not all the required fields are filled")

    def delete(self, request):
        data = request.query_params
        cv_id = data.get("id", None)
        if cv_id:
            cv = get_object_or_404(Cv, id=cv_id)
            cv.delete()
            return json_response_success("Cv deleted", status=204)
        return json_response_error("Id should be provided")


class SetGetVacation(APIView):
    permission_classes = (IsAuthenticated, PermsForVacation)

    def get(self, request):
        """
            parameters:
            - name: vacation_id
              required: false
              type: int
         """
        data = request.query_params
        vacation_id = data.get("vacation_id", None)
        if not vacation_id:
            vacation = [vac for vac in Vacation.objects.all().values()]
            return json_response_success(data=vacation)

        vacation = get_object_or_404(Vacation, pk=vacation_id)
        return json_response_success(data=model_to_dict(vacation))

    def put(self, request):
        """
            parameters:
            - name: id
              required: true
              type: int
            - name: comments
              description: comment to vacation
              required: false
              type: string
            - name: is_approved
              description: approve dev's vacation
              required: false
              type: bool
         """
        data = request.data
        from_date = data.get("from_date", None)
        to_date = data.get("to_date", None)
        comments = data.get("comments", None)
        is_approved = data.get("approved", False)
        vacation_id = data.get("id", None)

        if is_developer(request.user):
            dev_vacation_upd = get_object_or_404(Vacation, pk=vacation_id)
            dev_vacation_upd.from_date = from_date
            dev_vacation_upd.to_date = to_date
            dev_vacation_upd.save()

            return json_response_success("Vacation is updated. Feel free to contact a manager in order to approve it",
                                         status=200)

        if is_manager(request.user):
            dev_vacation_upd = get_object_or_404(Vacation, pk=vacation_id)
            dev_vacation_upd.from_date = from_date
            dev_vacation_upd.to_date = to_date
            dev_vacation_upd.comments = comments
            dev_vacation_upd.approved = is_approved
            dev_vacation_upd.save()

            return json_response_success("Vacation data has been changed", status=200)

        return json_response_error("Only 'MANAGER' or 'DEVELOPER' can update a vacations")

    def post(self, request):
        """
            parameters:
            - name: developer_id
              required: true
              type: int
            - name: from_date
              required: true
              type: string
            - name: to_date
              required: true
              type: string
            - name: is_approved
              description: approve dev's vacation
              required: false
              type: bool
         """
        data = request.data
        from_date = data.get("from_date", None)
        to_date = data.get("to_date", None)
        developer_id = data.get("developer_id", None)
        is_approved = data.get("is_approved", False)

        if not from_date and not to_date:
            return json_response_error("You must fill 'From date' and 'To date' fields")

        if is_developer(request.user):
            developer = get_object_or_404(Developer, user=request.user.id)
            dev_vacation = Vacation(from_date=from_date,
                                    to_date=to_date,
                                    developer=developer,
                                    approved=False,
                                    owner=request.user)
            dev_vacation.save()
            return json_response_success("Vacation is created. Feel free to contact a manager in order to approve it",
                                         status=201)

        if is_manager(request.user):
            developer = get_object_or_404(Developer, pk=developer_id)
            dev_vacation = Vacation(from_date=from_date,
                                    to_date=to_date,
                                    approved=is_approved,
                                    developer=developer,
                                    owner=request.user)
            dev_vacation.save()
            return json_response_success("You created the vacation for developer " +
                                         developer.surname + ' ' + developer.name, status=201)

        return json_response_success("Only 'MANAGER' or 'DEVELOPER' can create a vacations")

    def delete(self, request):
        data = request.data
        vacation_id = data.get("vacation_id", None)

        if vacation_id:
            if is_developer(request.user):
                developer = get_object_or_404(Developer, user=request.user.id)
                vacation = get_object_or_404(Vacation, id=vacation_id)
                if developer.id == vacation.developer.id:
                    vacation.delete()
                    return json_response_success("You deleted your vacation", status=204)
                return json_response_error("You can't delete vacation that is not yours")

            if is_manager(request.user):
                vacation = get_object_or_404(Vacation, id=vacation_id)
                vacation.delete()
                return json_response_success("Vacation deleted", status=204)
        return json_response_error("Please provide a vacation id")


class GetAllHolidays(APIView):
    permission_classes = (IsAuthenticated, PermsForVacation)

    def get(self, request):
        response = list()
        ua_holidays = get_ua_days_off(False)

        for project in Project.objects.all():
            if project.deadline or project.project_started_date:
                response.append(dict(title=project.name,
                                     start=project.project_started_date,
                                     end=project.deadline))

        for holiday in ua_holidays:
            response.append(dict(title=holiday.replace("_", " "),
                                 start=ua_holidays[holiday]))

        for developer in Developer.objects.all():
            response.append(dict(title=developer.name + " " + developer.surname + " Birthday",
                                 start=developer.birthday_date))

        for vacation in Vacation.objects.all():
            response.append(dict(title=vacation.developer.name + " " + vacation.developer.surname + " Vacation",
                                 start=vacation.from_date,
                                 end=vacation.to_date,
                                 id=vacation.id))

        return json_response_success(data=response)


class UserEndpoint(APIView):
    permission_classes = (IsAuthenticated, PermsForVacation)

    def get(self, request):
        users = [user for user in User.objects.all().values()]
        return json_response_success(data=users)

    def post(self, request):
        data = request.data

        user_name = data.get("user_name", None)
        user_password = data.get("password", None)
        user_role = data.get("user_role", None)

        if (not user_name) or (not user_password) or (not user_role):
            return json_response_error("You must fill 'User name', 'User password' and 'User role' fields")

        if user_role == "MANAGER":
            manager_name = data.get("first_name", None)
            manager_surname = data.get("last_name", None)
            manager_email = data.get("email", None)
            manager_position = data.get("position", None)
            manager_address = data.get("address", None)
            manager_company_name = data.get("company_name", None)

            user_manager = User.objects.create(username=user_name, password=make_password(user_password),
                                               user_type=user_role, email=manager_email, last_name=manager_surname,
                                               first_name=manager_name)
            manager = Manager.objects.create(
                name=manager_name,
                surname=manager_surname,
                email=manager_email,
                position=manager_position,
                address=manager_address,
                company_name=manager_company_name,
                user=user_manager
            )

            user_manager.save()
            manager.save()

            return json_response_success("Thank you for registration.", status=201)

        if user_role == "DEVELOPER":
            developer_name = data.get("first_name", None)
            developer_surname = data.get("last_name", None)
            developer_email = data.get("email", None)
            developer_hourly_rate = data.get("hourly_rate", None)
            developer_birthday_date = data.get("birthday_date", None)
            developer_monthly_salary = data.get("monthly_salary", None)

            user_developer = User.objects.create(username=user_name, password=make_password(user_password),
                                                 user_type=user_role, email=developer_email, last_name=developer_surname,
                                                 first_name=developer_name)
            developer = Developer.objects.create(
                name=developer_name,
                surname=developer_surname,
                email=developer_email,
                hourly_rate=developer_hourly_rate,
                birthday_date=developer_birthday_date,
                monthly_salary=developer_monthly_salary,
                user=user_developer
            )

            user_developer.save()
            developer.save()

            return json_response_success("Thank you for registration.", status=201)

        return json_response_error("You must provide all required fields.")


def get_acts(request):
    return render(request, 'core/act_of_perf_works_1.html')


class GenerateAct(APIView):
    permission_classes = ()

    def get(self, request):
        """
            parameters:
            - name: act_job_id
              required: false
              type: int
        """
        data = request.query_params
        act_job_id = data.get("act_job_id", None)
        if not act_job_id:
            acts = [act for act in ActOfPerfJobs.objects.all().values()]
            return json_response_success(data=acts)

        act = get_object_or_404(ActOfPerfJobs, id=act_job_id)
        return json_response_success(data=act)

    def post(self, request):
        data = request.data
        if set(data.keys()) == ACT_JOBS_REQUIRED_FIELDS:
            developer_id = data.get("developer_id", None)
            act_jobs_date = data.get("act_jobs_date", None)
            act_jobs_numb = data.get("act_jobs_numb", None)
            download = data.get("download", None)

            developer = Developer.objects.get(id=developer_id)
            customer = developer.customer
            try:
                dev_on_proj = DevelopersOnProject.objects.get(developer=developer)
            except DevelopersOnProject.DoesNotExist:
                dev_salary = developer.monthly_salary
            else:
                dev_salary = dev_on_proj.hours * developer.hourly_rate

            act_jobs = ActOfPerfJobs(date=act_jobs_date,
                                     number_of_act=act_jobs_numb,
                                     customer_info=customer,
                                     developer_info=developer)
            # do not save act_jobs() during dev
            # act_jobs.save()

            dev_bank_info = get_developer_bank_data(developer)
            cust_bank_info = get_customer_bank_data(customer)
            dev_salary_1 = dev_salary_2 = dev_salary / 2
            data = dict(developer_info=model_to_dict(developer),
                        act_jobs=model_to_dict(act_jobs),
                        customer_info=model_to_dict(customer),
                        total_salary=dev_salary,
                        dev_salary_1=dev_salary_1,
                        dev_salary_2=dev_salary_2,
                        dev_bank_info=dev_bank_info,
                        cust_bank_info=cust_bank_info)

            # return render(request, "core/act_of_perf_works_2(final).html", data)
            pdf_response, html = generate_pdf_from_html("core/act_of_perf_works_2(final).html", data)
            # commented not to send files to google drive during dev.
            # should be uncommented later.

            # pdf_to_google_drive(html)

            # if not download:
            #     data["company_details"]["sign"] = json.dumps(str(data["company_details"]["sign"]))
            #     return json_response_success(data=data)
            return HttpResponse(pdf_response.getvalue(), content_type='application/pdf')

        return json_response_error("Not all the required fields are filled up. %s are required."
                                   % ACT_JOBS_REQUIRED_FIELDS)

    def delete(self, request):
        data = request.data
        act_job_id = data.get("act_job_id", None)

        if act_job_id:
            act = get_object_or_404(ActOfPerfJobs, id=act_job_id)
            act.delete()
            return json_response_success("Act of performed jobs deleted", status=204)
        return json_response_error("Please provide act of performed jobs id")
