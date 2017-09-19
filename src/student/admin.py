from django.contrib import admin

from .models import StudentProfile, BoardOfEducation

class BoardOfEducationAdmin(admin.ModelAdmin):
	list_display = ('boe_id', 'boe_name' )
	fields = ('boe_name', )

class StudentProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'standard' , 'boe', 'roll_number')
	fields = ('user', 'standard', 'boe', 'roll_number')

admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(BoardOfEducation, BoardOfEducationAdmin)
