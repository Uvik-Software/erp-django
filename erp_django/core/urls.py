from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from rest_framework import viewsets, routers
from .models import Invoice, GeneralInfo, Project, Services
from .serializers import InvoiceSerializer, GeneralInfoSerializer, ProjectSerializer, ServicesSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class GeneralInfoViewSet(viewsets.ModelViewSet):
    queryset = GeneralInfo.objects.all()
    serializer_class = GeneralInfoSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer


router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'general_info', GeneralInfoViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'services', ServicesViewSet)

urlpatterns = [url(r'^', include(router.urls))] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
