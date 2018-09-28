from rest_framework.test import RequestsClient
from .models import ManagerInfo, Project, Invoice, Developer, Client, DevelopersOnProject, Company, User, Vacation, Cv
import pytest
import datetime
import json
import factory
from django.db.models import signals
from rest_framework.test import APIClient

BASE_URL = "http://127.0.0.1:8000"
CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

# TODO: fix tests. they are made long time ago for the first version of ERP
# TODO: verify restrictions for dif users in dif endpoints


class TestEndpoints:

    @factory.django.mute_signals(signals.post_save)
    @pytest.mark.django_db
    def setup(self):
        superuser = User.objects.create(username="uvik_main", password="some_password", is_superuser=True)
        manager_user = User.objects.create(username="uvik_manager", password="some_password", user_type="MANAGER")
        developer_user = User.objects.create(username="uvik_dev", password="some_password", user_type="DEVELOPER")

        # creating general info
        manager_info = ManagerInfo.objects.create(
            manager_name="some_name",
            manager_surname="some_surname",
            manager_email="manager_email@uvik.net",
            manager_position="manager",
            address="some_address",
            company_name="UVIK",
            owner=superuser
        )

        # creating developer
        developer = Developer.objects.create(
            name="some_developer_name",
            surname="some_developer_surname",
            email="some_dev_email@gmail.com",
            hourly_rate=35,
            birthday_date=CURRENT_DATE,
            monthly_salary=4500,
            user=developer_user
        )

        # creating client
        client = Client.objects.create(
            name="client_name",
            position="CEO",
            company_name="client's company name",
            address="client's address",
            email="client_email@gmail.com",
            phone="(063) 534 52 43",
            identification_number=1234567890,
            owner=manager_user
        )

        # creating project
        project = Project.objects.create(
            project_name="some_project_name",
            project_type="OUTSTAFF",
            project_description="some_project_description",
            currency="usd",
            manager_info=manager_info,
            client=client,
            owner=manager_user
        )

        # creating invoice
        invoice = Invoice.objects.create(
            date=CURRENT_DATE,
            expected_payout_date=CURRENT_DATE,
            project_id=project,
            status="WAITING_FOR_PAYMENT",
            owner=manager_user
        )

        # adding developer to project
        developer_on_project = DevelopersOnProject.objects.create(
            project=project,
            developer=developer,
            description="back end development",
            hours=132.4,
            owner=manager_user
        )

        # creating company info
        company = Company.objects.create(
            currency="usd",
            bank_account_number=12345533,
            beneficiary="some beneficiary",
            iban="CDK394848",
            swift="FSM93837",
            bank_address="some bank address",
            sign="some_url",
            owner=manager_user
        )

        vacation = Vacation.objects.create(
            developer=developer,
            from_date=CURRENT_DATE,
            to_date=CURRENT_DATE,
            comments="some comment",
            owner=manager_user
        )

        cv = Cv.objects.create(
            developer=developer,
            g_drive_link="http://somelinktoresume.com"
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

    def manager_happy_flow_post(self, endpoint, data):
        client = self.login_as_manager()
        response = client.post(BASE_URL + endpoint, data)
        assert response.status_code == 201

    def manager_happy_flow_get(self, endpoint, params=None):
        if params is None:
            params = ""
        else:
            params += "/"
        client = self.login_as_manager()
        response = client.get(BASE_URL + endpoint + params)
        assert response.status_code == 200
        return json.loads(response.content)

    def manager_happy_flow_put(self, endpoint, data):
        client = self.login_as_manager()
        response = client.put(BASE_URL + endpoint, data)
        assert response.status_code == 200
        return json.loads(response.content)

    def manager_happy_flow_put(self, endpoint, data):
        client = self.login_as_manager()
        response = client.put(BASE_URL + endpoint, data)
        assert response.status_code == 200
        return json.loads(response.content)

    def manager_happy_flow_delete(self, endpoint):
        client = self.login_as_manager()
        response = client.delete(BASE_URL + endpoint)
        assert response.status_code == 204

    @staticmethod
    def get_superuser():
        return User.objects.get(username='uvik_main')

    @staticmethod
    def get_manager():
        return User.objects.get(username='uvik_manager')

    @staticmethod
    def get_developer():
        return User.objects.get(username='uvik_developer')

    def login_as_superuser(self):
        user = self.get_superuser()
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def login_as_manager(self):
        user = self.get_manager()
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def login_as_developer(self):
        user = self.get_developer()
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    @pytest.mark.django_db
    def test_projects_general_info(self):
        project = Project.objects.get(project_name="some_project_name")
        manager_info = ManagerInfo.objects.get(manager_surname="some_surname")
        assert project.manager_info == manager_info

    @pytest.mark.django_db
    def test_manager_info_endpoint(self):
        user = self.get_manager()
        data = {"manager_name": "some_name",
                "manager_surname": "some_surname",
                "manager_email": "manager_email@gmail.com",
                "manager_position": "marketing manager",
                "address": "some_address",
                "company_name": "general info company name",
                "owner": user.id}

        self.manager_happy_flow_post("/manager_info/", data)

        response = self.manager_happy_flow_get("/manager_info/")
        assert len(response["results"]) == 2

        response = self.manager_happy_flow_get("/manager_info/", "2")
        assert set(response.items()).issubset(set(data.items())) is False

        data["manager_name"] = "another_name"
        response = self.manager_happy_flow_put("/manager_info/2/", data)
        assert response["manager_name"] == data["manager_name"]

        assert len([i for i in ManagerInfo.objects.all()]) == 2
        self.manager_happy_flow_delete("/manager_info/2/")
        assert len([i for i in ManagerInfo.objects.all()]) == 1

    """@pytest.mark.django_db
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


