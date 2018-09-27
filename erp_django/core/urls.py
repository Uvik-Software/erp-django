from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from rest_framework import routers
from .views import InvoiceViewSet, ManagerInfoViewSet, ProjectViewSet, ServicesViewSet, DeveloperViewSet, \
    DevelopersOnProjectViewSet, ClientViewSet, GenerateInvoice, DaysOff, CvSearch, schema_view, SetGetVacation


router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'general_info', ManagerInfoViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'services', ServicesViewSet)
router.register(r'developer', DeveloperViewSet)
router.register(r'developers_on_project', DevelopersOnProjectViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [url(r'', include(router.urls)),
               url(r'^generate_invoice/$', GenerateInvoice.as_view()),
               url(r'^days_off/$', DaysOff.as_view()),
               url(r'^cv_search/$', CvSearch.as_view()),
               url(r'^swagger/$', schema_view),
               url(r'^vacations/$', SetGetVacation.as_view())] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
