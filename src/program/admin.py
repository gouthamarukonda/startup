from django.contrib import admin

from .models import Program

class ProgramAdmin(admin.ModelAdmin):
	list_display = ('program_id', 'program_name', 'SUBJECTS')
	fields = ('program_name', )


admin.site.register(Program, ProgramAdmin)
