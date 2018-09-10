from rest_framework.test import RequestsClient
from .models import GeneralInfo, Project, Invoice, Services, Developer
import pytest
import datetime
import json

BASE_URL = "http://127.0.0.1:8000"
CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")


class TestEndpoints:

    @pytest.mark.django_db
    def setup(self):

        # creating general info
        general_info = GeneralInfo.objects.create(
            manager_name="some_name",
            manager_surname="some_surname",
            address="some_address",
            bank_requisites="some_bank_requisites"
        )

        # creating developer
        developer = Developer.objects.create(
            name="some_developer_name",
            surname="some_developer_surname",
            email="some_dev_email@gmail.com",
            hours=198.9
        )

        # creating project
        project = Project.objects.create(
            project_name="some_project_name",
            client_address="some_client_address",
            project_type="OUTSTAFF",
            currency="usd",
            basic_price="19.0",
            general_info=general_info,
            developer=developer
        )

        # creating invoice
        invoice = Invoice.objects.create(
            number=1234567890,
            date=CURRENT_DATE,
            expected_payout_date=CURRENT_DATE,
            project_id=project
        )

        # creating services for the invoice
        services = [{"price": 12.21, "quantity": 2, "invoice": invoice},
                    {"price": 14.71, "quantity": 7, "invoice": invoice},
                    {"price": 9.99, "quantity": 45, "invoice": invoice}]

        for service in services:
            Services.objects.create(
                price=service["price"],
                quantity=service["quantity"],
                invoice=service["invoice"]
            )

    @pytest.mark.django_db
    def test_invoice_services(self):
        invoice = Invoice.objects.get(number=1234567890)
        services = [service for service in Services.objects.filter(invoice=invoice)]
        assert len(services) == 3

    @pytest.mark.django_db
    def test_projects_general_info(self):
        project = Project.objects.get(project_name="some_project_name")
        general_info = GeneralInfo.objects.get(manager_surname="some_surname")
        assert project.general_info == general_info

    @pytest.mark.django_db
    def test_general_info_endpoint(self):
        data = {"manager_name": "some_name",
                "manager_surname": "some_surname",
                "address": "some_address",
                "bank_requisites": "some_bank_requisites"}

        client = RequestsClient()
        response = client.post(BASE_URL + "/general_info/", data)
        assert response.status_code == 201
        general_info = [info for info in GeneralInfo.objects.all()]
        assert len(general_info) == 2

        data.pop("address")
        response = client.post(BASE_URL + "/general_info/", data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_projects_endpoint(self):
        general_info = GeneralInfo.objects.get(manager_surname="some_surname")
        developer = Developer.objects.get(email="some_dev_email@gmail.com")
        data = {"project_name": "some_project_name",
                "client_address": "some_client_address",
                "project_type": "OUTSTAFF",
                "currency": "usd",
                "basic_price": 19.0,
                "general_info": general_info.id,
                "developer": developer.id}
        client = RequestsClient()
        response = client.post(BASE_URL + "/projects/", data)
        assert response.status_code == 201

        # test invalid project type
        data["project_type"] = 123453
        client = RequestsClient()
        response = client.post(BASE_URL + "/projects/", data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_invoice_endpoint(self):
        project = Project.objects.get(project_name="some_project_name")
        data = {"number": 1234567890,
                "date": CURRENT_DATE,
                "expected_payout_date": CURRENT_DATE,
                "project_id": project.id}
        client = RequestsClient()
        response = client.post(BASE_URL + "/invoices/", data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_services_endpoint(self):
        invoice = Invoice.objects.get(number=1234567890)
        data = {"price": 12.3,
                "quantity": 2,
                "invoice": invoice.id}
        client = RequestsClient()
        response = client.post(BASE_URL + "/services/", data)
        assert response.status_code == 201

        # test total cost
        response_data = json.loads(response.content)
        assert response_data["total_cost"] == data["price"] * data["quantity"]

    @pytest.mark.django_db
    def test_developer_endpoint(self):
        data = {"name": "some_developer_name",
                "surname": "some_developer_surname",
                "email": "some_dev_email2@gmail.com",
                "hours": 198.9}
        client = RequestsClient()
        response = client.post(BASE_URL + "/developer/", data)
        assert response.status_code == 201

        # providing existing email. should fail as it should be unique
        data["email"] = "some_dev_email2@gmail.com"
        response = client.post(BASE_URL + "/developer/", data)
        assert response.status_code == 400

        # providing email in a wrong format
        data["email"] = "some_dev_email"
        response = client.post(BASE_URL + "/developer/", data)
        assert response.status_code == 400

