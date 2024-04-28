from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'usn', 'email', 'phone_number', 'is_active']
    list_editable = ['is_active']



admin.site.register(User, UserAdmin)
