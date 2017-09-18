from django.contrib import admin

from .models import Paper

class PaperAdmin(admin.ModelAdmin):
	list_display = ('paper_id', 'program', 'standard', 'INSTITUTES', 'QUESTIONS', 'paper_name', 'paper_type', 'teacher_id', 'start_time', 'end_time', 'duration', 'partial_marking' , 'time_stamp')
	fields = ('program', 'standard', 'paper_name', 'paper_type', 'teacher_id', 'start_time', 'end_time' , 'duration', 'partial_marking')

admin.site.register(Paper, PaperAdmin)
