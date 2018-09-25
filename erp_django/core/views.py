from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse, HttpResponse

from django.forms.models import model_to_dict
from .models import Invoice, ManagerInfo, Project, Services, Developer, DevelopersOnProject, Client, Company, \
    SentNotifications, BirthdayNotification, User
from .serializers import InvoiceSerializer, ManagerInfoSerializer, ProjectSerializer, ServicesSerializer, \
    DeveloperSerializer, DevelopersOnProjectSerializer, ClientSerializer

from .utils import pdf_to_google_drive, generate_pdf_from_html, get_project_developers_and_cost, \
    get_project_details, get_company_details_by_currency, gmail_sender, is_manager
from .constants import INVOICE_REQUIRED_FIELDS
import json


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)


class ManagerInfoViewSet(viewsets.ModelViewSet):
    queryset = ManagerInfo.objects.all()
    serializer_class = ManagerInfoSerializer
    permission_classes = (IsAuthenticated,)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)


class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (IsAuthenticated,)


class ClientViewSet(viewsets.ModelViewSet):
    from .permissions import CustomObjectPermissions, IsOwnerOrReadOnly
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class DevelopersOnProjectViewSet(viewsets.ModelViewSet):
    queryset = DevelopersOnProject.objects.all()
    serializer_class = DevelopersOnProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        project_id = self.request.GET.get('project_id', None)
        if project_id:
            return DevelopersOnProject.objects.all().filter(project_id=project_id)

        return DevelopersOnProject.objects.all()


class GenerateInvoice(APIView):
    permission_classes = (IsAuthenticated,)

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
                return JsonResponse(data)
            return HttpResponse(pdf_response.getvalue(), content_type='application/pdf')

        return JsonResponse({"status": "Not all the required fields are filled up. %s are required."
                                       % INVOICE_REQUIRED_FIELDS})


class Draft(APIView):
    from .permissions import CustomObjectPermissions
    permission_classes = (CustomObjectPermissions,)

    def get_queryset(self):
        from .models import User
        user = User.objects.get(id=3)
        print("here", user.has_perm("core.change_client"))
        print(user.__dict__)
        #all_model_perms = [perm for perm in get_perms_for_model(Client)]
        #print(all_model_perms)
        #return get_objects_for_user(self.request.user, all_model_perms)
        #import pdb
        #pdb.set_trace()
        #assign_perm("core.view_client", user)
        return User.objects.all()
