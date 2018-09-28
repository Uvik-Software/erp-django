from rest_framework import serializers
from .models import ManagerInfo, Project, Invoice, Developer, DevelopersOnProject, Client, Vacation


class InvoiceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Invoice
        fields = "__all__"


class ManagerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ManagerInfo
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = "__all__"


class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = "__all__"


class DevelopersOnProjectSerializer(serializers.ModelSerializer):
    developer_name = serializers.CharField(source='developer.name', read_only=True)
    developer_surname = serializers.CharField(source='developer.surname', read_only=True)
    developer_email = serializers.EmailField(source='developer.email', read_only=True)
    #developer_hours = serializers.FloatField(source='developer.hours', read_only=True)
    developer_hourly_rate = serializers.IntegerField(source='developer.hourly_rate', read_only=True)

    project_name = serializers.CharField(source='project.project_name', read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = DevelopersOnProject
        #depth = 1
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Client
        fields = "__all__"


class VacationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Vacation
        fields = "__all__"
