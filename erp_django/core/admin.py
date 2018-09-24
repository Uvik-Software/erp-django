from django.contrib import admin
from .models import Company
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets += ('Account Type', {'fields': ('user_type',)}),

admin.site.register(Company)
admin.site.register(User, UserAdmin)
