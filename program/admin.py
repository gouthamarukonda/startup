from django.contrib import admin

from .models import Program, Standard

class ProgramAdmin(admin.ModelAdmin):
	list_display = ('program_id', 'program_name', 'SUBJECTS')
	fields = ('program_name', )

class StandardAdmin(admin.ModelAdmin):
	list_display = ('standard_id', 'standard_name')
	fields = ('standard_name', )

admin.site.register(Program, ProgramAdmin)
admin.site.register(Standard, StandardAdmin)
