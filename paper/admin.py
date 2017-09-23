from django.contrib import admin

from .models import Paper, PaperType

class PaperTypeAdmin(admin.ModelAdmin):
	list_display = ('type_id', 'type_name')
	fields = ('type_name', )
		
class PaperAdmin(admin.ModelAdmin):
	list_display = ('paper_id', 'program', 'STANDARDS', 'INSTITUTES', 'QUESTIONS', 'paper_name', 'paper_type', 'teacher_id', 'start_time', 'end_time', 'duration', 'partial_marking' , 'time_stamp')
	fields = ('program', 'paper_name', 'paper_type', 'teacher_id', 'start_time', 'end_time' , 'duration', 'partial_marking')

admin.site.register(Paper, PaperAdmin)
admin.site.register(PaperType, PaperTypeAdmin)
