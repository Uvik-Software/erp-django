from rest_framework import serializers
from .models import Manager, Project, Invoice, Developer, DevelopersOnProject, Client, Vacation, User, ActOfPerfJobs, \
    Owner


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
        fields = ('id', 'first_name', 'last_name', 'email', 'hourly_rate', 'monthly_salary', 'birthday_date',)


class DevelopersOnProjectSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='developer.first_name', read_only=True)
    last_name = serializers.CharField(source='developer.last_name', read_only=True)
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
        fields = ('id', 'first_name', 'last_name', 'position', 'email', 'phone', 'identification_number', 'address',
                  'company_name',)


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


class OwnerSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Owner
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'position', 'id',)


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'birthday_date', 'email', 'additional_info', 'tax_number',
                  'phone',)
