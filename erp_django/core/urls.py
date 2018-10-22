from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from rest_framework import routers
from .views import InvoiceViewSet, ManagerViewSet, ProjectViewSet, DeveloperViewSet, \
    DevelopersOnProjectViewSet, ClientViewSet, GenerateInvoice, DaysOff, DevelopersCv, schema_view, SetGetVacation, \
    DashboardReport, UserEndpoint, GetAllHolidays
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'developers', DeveloperViewSet)
router.register(r'developers_on_project', DevelopersOnProjectViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [url(r'', include(router.urls)),
               url(r'^auth-jwt/', obtain_jwt_token),
               url(r'^auth-jwt-refresh/', refresh_jwt_token),
               url(r'^auth-jwt-verify/', verify_jwt_token),
               url(r'^generate_invoice/$', GenerateInvoice.as_view()),
               url(r'^days_off/$', DaysOff.as_view()),
               url(r'^cv/$', DevelopersCv.as_view()),
               url(r'^swagger/$', schema_view),
               url(r'^vacations/$', SetGetVacation.as_view()),
               url(r'^users/$', UserEndpoint.as_view()),
               url(r'^dashboard_report/$', DashboardReport.as_view()),
               url(r'^all_holidays/$', GetAllHolidays.as_view())] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
