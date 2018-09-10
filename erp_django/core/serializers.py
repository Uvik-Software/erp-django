from rest_framework import serializers
from .models import GeneralInfo, Project, Invoice, Services, Developer


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = "__all__"


class GeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralInfo
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"


class ServicesSerializer(serializers.ModelSerializer):
    total_cost = serializers.ReadOnlyField()

    class Meta:
        model = Services
        fields = "__all__"


class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = "__all__"
