from django.contrib import admin

# Register your models here.

from .models import Institute

class InstituteAdmin(admin.ModelAdmin):
	list_display = ('institute_id', 'institute_name', 'address', 'city', 'state', 'phone_no', 'manager_name')
	fields = ('institute_name', 'address', 'city', 'state', 'phone_no', 'manager_name')

admin.site.register(Institute, InstituteAdmin)