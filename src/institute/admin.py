from django.contrib import admin

from .models import Institute
from .models2 import InstituteAdmin

class InstituteModelAdmin(admin.ModelAdmin):
	list_display = ('institute_id', 'institute_name', 'address', 'city', 'state', 'phone_no', 'manager_name')
	fields = ('institute_name', 'address', 'city', 'state', 'phone_no', 'manager_name')

class InstituteAdminModelAdmin(admin.ModelAdmin):
	list_display = ('user',)

admin.site.register(Institute, InstituteModelAdmin)
admin.site.register(InstituteAdmin, InstituteAdminModelAdmin)
