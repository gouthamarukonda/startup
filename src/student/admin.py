from django.contrib import admin

from .models import StudentProfile

class StudentProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'standard' , 'boe', 'roll_number', 'address')
	fields = ('user', 'standard', 'boe', 'roll_number', 'address')

admin.site.register(StudentProfile, StudentProfileAdmin)
