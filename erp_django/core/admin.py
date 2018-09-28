from django.contrib import admin
from .models import Company
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Developer, ManagerInfo, Project, Vacation, Client

UserAdmin.fieldsets += ('Account Type', {'fields': ('user_type',)}),

admin.site.register(Company)
admin.site.register(User, UserAdmin)
admin.site.register(Developer)
admin.site.register(ManagerInfo)
admin.site.register(Project)
admin.site.register(Vacation)
admin.site.register(Client)
