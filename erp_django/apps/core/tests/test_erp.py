# from rest_framework.test import RequestsClient
# from core.models import Manager, Project, Invoice, Developer, Client, DevelopersOnProject, Company, User, Vacation, Cv, \
#     Owner
# import pytest
# import datetime
# import json
# import factory
# from django.db.models import signals
# from rest_framework.test import APIClient
#
# BASE_URL = "http://127.0.0.1:8000"
# CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
#
# # TODO: fix tests. they are made long time ago for the first version of ERP
# # TODO: verify restrictions for dif users in dif endpoints
#
#
# class TestEndpoints:
#
#     @factory.django.mute_signals(signals.post_save)
#     @pytest.mark.django_db
#     def setup(self):
#         superuser = User.objects.create(username="uvik_main", password="some_password", is_superuser=True, is_staff=True)
#
#         # creating general info
#         owner = Owner.objects.create()
#         manager_info = Manager.objects.create(
#             username="uvik_manager",
#             password="some_password",
#             type="MANAGER",
#             first_name="some_name",
#             last_name="some_surname",
#             email="manager_email@uvik.net",
#             position="manager",
#             address="some_address",
#             company_name="UVIK",
#         )
#
#         # creating developer
#         developer = Developer.objects.create(
#             username="uvik_dev",
#             password="some_password",
#             type="DEVELOPER",
#             first_name="some_developer_name",
#             last_name="some_developer_surname",
#             email="some_dev_email@gmail.com",
#             hourly_rate=35,
#             birthday_date=CURRENT_DATE,
#             monthly_salary=4500,
#         )
#
#         # creating client
#         client = Client.objects.create(
#             first_name="client_name",
#             position="CEO",
#             company_name="client's company name",
#             address="client's address",
#             email="client_email@gmail.com",
#             phone="(063) 534 52 43",
#             identification_number=1234567890,
#             owner=owner
#         )
#
#         # creating project
#         project = Project.objects.create(
#             project_name="some_project_name",
#             project_type="OUTSTAFF",
#             project_description="some_project_description",
#             currency="usd",
#             manager_info=manager_info,
#             client=client,
#             owner=owner
#         )
#
#         # creating invoice
#         invoice = Invoice.objects.create(
#             date=CURRENT_DATE,
#             expected_payout_date=CURRENT_DATE,
#             project_id=project.id,
#             status="WAITING_FOR_PAYMENT",
#             owner=owner
#         )
#
#         # adding developer to project
#         developer_on_project = DevelopersOnProject.objects.create(
#             project=project,
#             developer=developer,
#             description="back end development",
#             hours=132.4,
#             owner=owner
#         )
#
#         # creating company info
#         company = Company.objects.create(
#             currency="usd",
#             bank_account_number=12345533,
#             beneficiary="some beneficiary",
#             iban="CDK394848",
#             swift="FSM93837",
#             bank_address="some bank address",
#             sign="some_url",
#             owner=owner
#         )
#
#         vacation = Vacation.objects.create(
#             user=developer,
#             from_date=CURRENT_DATE,
#             to_date=CURRENT_DATE,
#             comments="some comment"
#         )
#
#         cv = Cv.objects.create(
#             developer=developer,
#             g_drive_link="http://somelinktoresume.com"
#         )
#
#     def verify_missing_data(self, endpoint, data):
#         client = self.login_as_manager()
#         for key in data.keys():
#             temp = data[key]
#             data.pop(key)
#             response = client.post(BASE_URL + endpoint, data)
#             data[key] = temp
#             assert response.status_code == 400
#
#     def manager_happy_flow_post(self, endpoint, data):
#         client = self.login_as_manager()
#         response = client.post(BASE_URL + endpoint, data)
#         assert response.status_code == 201
#
#     def manager_happy_flow_get(self, endpoint, params=None):
#         if params is None:
#             params = ""
#         else:
#             params += "/"
#         client = self.login_as_manager()
#         response = client.get(BASE_URL + endpoint + params)
#         assert response.status_code == 200
#         return json.loads(response.content)
#
#     def manager_happy_flow_put(self, endpoint, data):
#         client = self.login_as_manager()
#         response = client.put(BASE_URL + endpoint, data)
#         assert response.status_code == 200
#         return json.loads(response.content)
#
#     def manager_happy_flow_delete(self, endpoint):
#         client = self.login_as_manager()
#         response = client.delete(BASE_URL + endpoint)
#         assert response.status_code == 204
#
#     def dev_happy_flow_get(self, endpoint, params=None):
#         if params is None:
#             params = ""
#         else:
#             params += "/"
#         client = self.login_as_manager()
#         response = client.get(BASE_URL + endpoint + params)
#         assert response.status_code == 200
#         return json.loads(response.content)
#
#     def dev_happy_flow_put(self, endpoint, data):
#         client = self.login_as_manager()
#         response = client.put(BASE_URL + endpoint, data)
#         assert response.status_code == 200
#         return json.loads(response.content)
#
#     def dev_happy_flow_post(self, endpoint, data):
#         client = self.login_as_manager()
#         response = client.post(BASE_URL + endpoint, data)
#         assert response.status_code == 200
#         return json.loads(response.content)
#
#     def dev_happy_flow_delete(self, endpoint):
#         client = self.login_as_manager()
#         response = client.delete(BASE_URL + endpoint)
#         assert response.status_code == 204
#
#     def restricted_dev_get(self, endpoint, params=None):
#         if params is None:
#             params = ""
#         else:
#             params += "/"
#         client = self.login_as_developer()
#         response = client.get(BASE_URL + endpoint + params)
#         assert response.status_code == 403
#
#     def restricted_dev_put(self, endpoint, data):
#         client = self.login_as_developer()
#         response = client.put(BASE_URL + endpoint, data)
#         assert response.status_code == 403
#
#     def restricted_dev_post(self, endpoint, data):
#         client = self.login_as_developer()
#         response = client.post(BASE_URL + endpoint, data)
#         assert response.status_code == 403
#
#     def restricted_dev_delete(self, endpoint):
#         client = self.login_as_developer()
#         response = client.delete(BASE_URL + endpoint)
#         assert response.status_code == 403
#
#     @staticmethod
#     def get_superuser():
#         return User.objects.get(username='uvik_main')
#
#     @staticmethod
#     def get_manager():
#         return User.objects.get(username='uvik_manager')
#
#     @staticmethod
#     def get_developer():
#         return User.objects.get(username='uvik_dev')
#
#     def login_as_superuser(self):
#         user = self.get_superuser()
#         client = APIClient()
#         client.force_authenticate(user=user)
#         return client
#
#     def login_as_manager(self):
#         user = self.get_manager()
#         client = APIClient()
#         client.force_authenticate(user=user)
#         return client
#
#     def login_as_developer(self):
#         user = self.get_developer()
#         client = APIClient()
#         client.force_authenticate(user=user)
#         return client
#
#     @pytest.mark.django_db
#     def test_projects_general_info(self):
#         project = Project.objects.get(project_name="some_project_name")
#         manager_info = Manager.objects.get(surname="some_surname")
#         assert project.manager_info == manager_info
#
#     @pytest.mark.django_db
#     def test_manager_info_endpoint(self):
#         user = self.get_manager()
#         data = {"name": "some_name",
#                 "surname": "some_surname",
#                 "email": "manager_email@gmail.com",
#                 "position": "marketing manager",
#                 "address": "some_address",
#                 "company_name": "general info company name",
#                 "owner": user.id}
#
#         self.manager_happy_flow_post("/manager_info/", data)
#
#         response = self.manager_happy_flow_get("/manager_info/")
#         assert len(response["results"]) == 2
#
#         response = self.manager_happy_flow_get("/manager_info/", "2")
#         assert set(response.items()).issubset(set(data.items())) is False
#
#         data["name"] = "another_name"
#         response = self.manager_happy_flow_put("/manager_info/2/", data)
#         assert response["name"] == data["name"]
#
#         assert len([i for i in Manager.objects.all()]) == 2
#         self.manager_happy_flow_delete("/manager_info/2/")
#         assert len([i for i in Manager.objects.all()]) == 1
#
#         self.restricted_dev_get("/manager_info/")
#         self.restricted_dev_post("/manager_info/", data)
#         self.restricted_dev_put("/manager_info/1/", data)
#         self.restricted_dev_delete("/manager_info/1/")
#         assert len([i for i in Manager.objects.all()]) == 1
#
#     @pytest.mark.django_db
#     def test_projects_endpoint(self):
#         manager_info = Manager.objects.get(surname="some_surname")
#         client = Client.objects.get(email="client_email@gmail.com")
#         user = self.get_manager()
#         data = {"project_name": "some_project_name",
#                 "project_type": "OUTSTAFF",
#                 "project_description": "bugs fixes",
#                 "currency": "usd",
#                 "basic_price": 19.0,
#                 "manager_info": manager_info.id,
#                 "client": client.id,
#                 "owner": user.id}
#         self.manager_happy_flow_post("/projects/", data)
#         self.manager_happy_flow_put("/projects/2/", data)
#         self.manager_happy_flow_get("/projects/1/")
#         self.manager_happy_flow_delete("/projects/2/")
#
#         # test invalid project type
#         data["project_type"] = 123453
#         client = self.login_as_manager()
#         response = client.post(BASE_URL + "/projects/", data)
#         assert response.status_code == 400
#
#         self.verify_missing_data("/projects/", data)
#
#         self.restricted_dev_get("/projects/")
#         self.restricted_dev_post("/projects/", data)
#         self.restricted_dev_put("/projects/1/", data)
#         self.restricted_dev_delete("/projects/1/")
#
#     @pytest.mark.django_db
#     def test_invoice_endpoint(self):
#         project = Project.objects.get(project_name="some_project_name")
#         user = self.get_manager()
#         data = {"date": CURRENT_DATE,
#                 "expected_payout_date": CURRENT_DATE,
#                 "project_id": project.id,
#                 "status": "PAID",
#                 "owner": user.id}
#         self.manager_happy_flow_post("/invoices/", data)
#         self.manager_happy_flow_put("/invoices/2/", data)
#         self.manager_happy_flow_get("/invoices/1/")
#         self.manager_happy_flow_delete("/invoices/2/")
#
#         self.verify_missing_data("/invoices/", data)
#
#         self.restricted_dev_get("/invoices/")
#         self.restricted_dev_post("/invoices/", data)
#         self.restricted_dev_put("/invoices/1/", data)
#         self.restricted_dev_delete("/invoices/1/")
#
#     @factory.django.mute_signals(signals.post_save)
#     @pytest.mark.django_db
#     def test_developer_endpoint(self):
#         developer_user = self.get_developer()
#         data = {"name": "some_developer_name",
#                 "surname": "some_developer_surname",
#                 "email": "some_dev_email2@gmail.com",
#                 "hourly_rate": 35,
#                 "birthday_date": CURRENT_DATE,
#                 "monthly_salary": 4500,
#                 "user": developer_user.id
#         }
#         self.manager_happy_flow_post("/developer/", data)
#         self.manager_happy_flow_put("/developer/2/", data)
#         self.manager_happy_flow_get("/developer/1/")
#         self.manager_happy_flow_delete("/developer/2/")
#
#         self.verify_missing_data("/developer/", data)
#
#         self.restricted_dev_get("/developer/")
#         self.restricted_dev_post("/developer/", data)
#         self.restricted_dev_put("/developer/1/", data)
#         self.restricted_dev_delete("/developer/1/")
#
#     @pytest.mark.django_db
#     def test_developers_on_project_endpoint(self):
#         project = Project.objects.get(id=1)
#         developer = Developer.objects.get(id=1)
#         user = self.get_manager()
#         data = {"project": project.id,
#                 "developer": developer.id,
#                 "description": "bugs fixes",
#                 "hours": 143.8,
#                 "owner": user.id}
#         self.manager_happy_flow_post("/developers_on_project/", data)
#         self.manager_happy_flow_put("/developers_on_project/2/", data)
#         self.manager_happy_flow_get("/developers_on_project/1/")
#         self.manager_happy_flow_delete("/developers_on_project/2/")
#
#         self.restricted_dev_get("/developers_on_project/")
#         self.restricted_dev_post("/developers_on_project/", data)
#         self.restricted_dev_put("/developers_on_project/1/", data)
#         self.restricted_dev_delete("/developers_on_project/1/")
#
#     @pytest.mark.django_db
#     def test_cv_endpoint(self):
#         developer = Developer.objects.all().first()
#         data = {"cv_link": "http://some_link.com/",
#                 "dev_id": developer.id}
#         self.manager_happy_flow_post("/cv/", data)
#         self.manager_happy_flow_put("/cv/?id=2", data)
#         self.manager_happy_flow_get("/cv/?id=2/")
#         self.manager_happy_flow_get("/cv/")
#         self.manager_happy_flow_delete("/cv/?id=2")
