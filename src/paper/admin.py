from django.contrib import admin

from .models import Paper
from .models import Mapping

class PaperAdmin(admin.ModelAdmin):
	list_display = ('paper_id', 'program', 'paper_name', 'paper_type', 'teacher_id', 'start_time', 'end_time' , 'partial_marking' , 'time_stamp')
	fields = ('program', 'paper_name', 'paper_type', 'teacher_id', 'start_time', 'end_time' , 'partial_marking')

class MappingAdmin(admin.ModelAdmin):
	list_display = ('map_id', 'question', 'paper')
	fields = ('question', 'paper')

admin.site.register(Paper, PaperAdmin)
admin.site.register(Mapping, MappingAdmin)
