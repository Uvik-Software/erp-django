from rest_framework.test import RequestsClient
from .models import ManagerInfo, Project, Invoice, Developer, Client, DevelopersOnProject, Company, User
import pytest
import datetime
import json

BASE_URL = "http://127.0.0.1:8000"
CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

# TODO: fix tests. they are made long time ago for the first version of ERP


class TestEndpoints:

    @pytest.mark.django_db
    def setup(self):
        superuser = User.objects.create(username="uvik_main", password="some_password", is_superuser=True)
        manager = User.objects.create(username="uvik_manager", password="some_password", user_type="MANAGER")
        developer = User.objects.create(username="uvik_dev", password="some_password", user_type="DEVELOPER")

        # creating general info
        manager_info = ManagerInfo.objects.create(
            manager_name="some_name",
            manager_surname="some_surname",
            manager_email="manager_email@uvik.net",
            manager_position="manager",
            address="some_address",
            company_name="UVIK"
        )

        # creating developer
        developer = Developer.objects.create(
            name="some_developer_name",
            surname="some_developer_surname",
            email="some_dev_email@gmail.com",
            hourly_rate=35,
            birthday_date=CURRENT_DATE,
            monthly_salary=4500,
            user=manager.id
        )

        # creating client
        client = Client.objects.create(
            name="client_name",
            position="CEO",
            company_name="client's company name",
            address="client's address",
            email="client_email@gmail.com",
            phone="(063) 534 52 43",
            identification_number=1234567890
        )

        # creating project
        project = Project.objects.create(
            project_name="some_project_name",
            project_type="OUTSTAFF",
            project_description="some_project_description",
            currency="usd",
            manager_info=manager_info,
            client=client
        )

        # creating invoice
        """invoice = Invoice.objects.create(
            date=CURRENT_DATE,
            expected_payout_date=CURRENT_DATE,
            project_id=project
        )

        # adding developer to project
        developer_on_project = DevelopersOnProject.objects.create(
            project=project,
            developer=developer,
            description="back end development",
            hours=132.4
        )

        # creating company info
        company = Company.objects.create(
            currency="usd",
            bank_account_number=12345533,
            beneficiary="some beneficiary",
            iban="CDK394848",
            swift="FSM93837",
            bank_address="some bank address",
            sign="some_url"
        )

    @staticmethod
    def verify_missing_data(endpoint, data):
        client = RequestsClient()
        for key in data.keys():
            temp = data[key]
            data.pop(key)
            response = client.post(BASE_URL + endpoint, data)
            data[key] = temp
            assert response.status_code == 400

    @staticmethod
    def happy_flow(endpoint, data):
        client = RequestsClient()
        response = client.post(BASE_URL + endpoint, data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_projects_general_info(self):
        project = Project.objects.get(project_name="some_project_name")
        general_info = ManagerInfo.objects.get(manager_surname="some_surname")
        assert project.general_info == general_info"""

    """@pytest.mark.django_db
    def test_manager_info_endpoint(self):
        data = {"manager_name": "some_name",
                "manager_surname": "some_surname",
                "manager_email": "manager_email@gmail.com",
                "manager_position": "marketing manager",
                "address": "some_address",
                "company_name": "general info company name"}

        client = RequestsClient()
        response = client.post(BASE_URL + "/general_info/", data)
        assert response.status_code == 201
        general_info = [info for info in GeneralInfo.objects.all()]
        assert len(general_info) == 2

        self.verify_missing_data("/general_info/", data)

    @pytest.mark.django_db
    def test_projects_endpoint(self):
        general_info = GeneralInfo.objects.get(manager_surname="some_surname")
        client = Client.objects.get(email="client_email@gmail.com")
        data = {"project_name": "some_project_name",
                "project_type": "OUTSTAFF",
                "project_description": "bugs fixes",
                "currency": "usd",
                "basic_price": 19.0,
                "general_info": general_info.id,
                "client": client.id}
        self.happy_flow("/projects/", data)

        # test invalid project type
        data["project_type"] = 123453
        client = RequestsClient()
        response = client.post(BASE_URL + "/projects/", data)
        assert response.status_code == 400

        self.verify_missing_data("/projects/", data)

    @pytest.mark.django_db
    def test_invoice_endpoint(self):
        project = Project.objects.get(project_name="some_project_name")
        data = {"date": CURRENT_DATE,
                "expected_payout_date": CURRENT_DATE,
                "project_id": project.id}
        self.happy_flow("/invoices/", data)

        self.verify_missing_data("/invoices/", data)

    @pytest.mark.django_db
    def test_services_endpoint(self):
        invoice = Invoice.objects.get(id=1)
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
                "hourly_rate": 35}
        self.happy_flow("/developer/", data)

        client = RequestsClient()
        # providing existing email. should fail as it should be unique
        data["email"] = "some_dev_email2@gmail.com"
        response = client.post(BASE_URL + "/developer/", data)
        assert response.status_code == 400

        # providing email in a wrong format
        data["email"] = "some_dev_email"
        response = client.post(BASE_URL + "/developer/", data)
        assert response.status_code == 400

        self.verify_missing_data("/developer/", data)

    @pytest.mark.django_db
    def test_developers_on_project_endpoint(self):
        project = Project.objects.get(id=1)
        developer = Developer.objects.get(id=1)
        data = {"project": project.id,
                "developer": developer.id,
                "description": "bugs fixes",
                "hours": 143.8}
        self.happy_flow("/developers_on_project/", data)"""


