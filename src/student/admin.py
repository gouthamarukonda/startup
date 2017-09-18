from django.contrib import admin

from .models import StudentProfile

class StudentProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'standard' , 'boe', 'roll_number')
	fields = ('user', 'standard', 'boe', 'roll_number')

admin.site.register(StudentProfile, StudentProfileAdmin)
