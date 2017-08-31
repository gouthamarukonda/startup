from django.contrib import admin

from .models import StudentProfile

class StudentProfileAdmin(admin.ModelAdmin):
	list_display = ( 'user', 'standard' , 'boe')
	fields = ( 'user', 'standard', 'boe')

admin.site.register(StudentProfile, StudentProfileAdmin)
