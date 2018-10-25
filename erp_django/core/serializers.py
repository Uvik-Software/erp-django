from rest_framework import serializers
from .models import Manager, Project, Invoice, Developer, DevelopersOnProject, Client, Vacation, User, ActOfPerfJobs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Invoice
        fields = "__all__"


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        #depth = 1
        fields = "__all__"


class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Developer
        fields = "__all__"


class DevelopersOnProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='developer.name', read_only=True)
    surname = serializers.CharField(source='developer.surname', read_only=True)
    email = serializers.EmailField(source='developer.email', read_only=True)
    #developer_hours = serializers.FloatField(source='developer.hours', read_only=True)
    hourly_rate = serializers.IntegerField(source='developer.hourly_rate', read_only=True)

    project_name = serializers.CharField(source='project.project_name', read_only=True)
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = DevelopersOnProject
        #depth = 1
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Client
        fields = "__all__"


class VacationSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Vacation
        fields = "__all__"


class ActOfPerfJobsSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = ActOfPerfJobs
        fields = "__all__"
