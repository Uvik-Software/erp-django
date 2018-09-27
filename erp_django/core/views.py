from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework import viewsets, renderers, schemas, response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .permissions import ManagerFullAccess

from django.http import HttpResponse

from django.forms.models import model_to_dict
from .models import Invoice, ManagerInfo, Project, Services, Developer, DevelopersOnProject, Client, Cv
from .serializers import InvoiceSerializer, ManagerInfoSerializer, ProjectSerializer, ServicesSerializer, \
    DeveloperSerializer, DevelopersOnProjectSerializer, ClientSerializer

from .utils import pdf_to_google_drive, generate_pdf_from_html, get_project_developers_and_cost, \
    get_project_details, get_company_details_by_currency, gmail_sender, is_manager, get_ua_days_off, \
    json_response_error, json_response_success
from .constants import INVOICE_REQUIRED_FIELDS
import json
from rest_framework.schemas import AutoSchema
import coreapi


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes((AllowAny,))
def schema_view(request):
    generator = schemas.SchemaGenerator(
        title='UVIK ERP API end points')
    return response.Response(generator.get_schema(request=request))


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class ManagerInfoViewSet(viewsets.ModelViewSet):
    queryset = ManagerInfo.objects.all()
    serializer_class = ManagerInfoSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, ManagerFullAccess)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DevelopersOnProjectViewSet(viewsets.ModelViewSet):
    queryset = DevelopersOnProject.objects.all()
    serializer_class = DevelopersOnProjectSerializer
    permission_classes = (IsAuthenticated, ManagerFullAccess)

    def get_queryset(self):
        project_id = self.request.GET.get('project_id', None)
        if project_id:
            return DevelopersOnProject.objects.all().filter(project_id=project_id)

        return DevelopersOnProject.objects.all()


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
            general_info = ManagerInfo.objects.get(id=project.general_info.id)
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
                        general_info=model_to_dict(general_info),
                        total_cost=total_cost)

            pdf_response, html = generate_pdf_from_html("invoices/invoice_2.html", data)
            #pdf_to_google_drive(html)
            #gmail_sender(html, client_info.email, "Invoice")

            if not download:
                data["company_details"]["sign"] = json.dumps(str(data["company_details"]["sign"]))
                return json_response_success(data)
            return HttpResponse(pdf_response.getvalue(), content_type='application/pdf')

        return json_response_error("Not all the required fields are filled up. %s are required."
                                       % INVOICE_REQUIRED_FIELDS)

# TODO: add swagger for other APIViews. https://github.com/m-haziq/django-rest-swagger-docs can help


class DaysOff(APIView):
    permission_classes = (IsAuthenticated, ManagerFullAccess,)

    def get(self, request):
        # TODO: can be added a param to show all holidays till the end of the year
        next_month_days_off = get_ua_days_off()
        return json_response_success(next_month_days_off)

    def post(self, request):
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


class CvSearch(APIView):
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
        data = request.query_params

        if "name" in data:
            cv = [cv for cv in Cv.objects.filter(developer__name__contains=data["name"]).values()]
            return json_response_success(cv)
        if "surname" in data:
            cv = [cv for cv in Cv.objects.filter(developer__surname__contains=data["surname"]).values()]
            return json_response_success(cv)

        return json_response_error("Should provide name or surname")
