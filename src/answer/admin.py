from django.contrib import admin

from .models import Answer

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('answer_id', 'question', 'attempt', 'status', 'time_taken', 'answer_array' , 'int_answer' , 'marks_obtained' , 'time_stamp')
	fields = ('question', 'attempt', 'status', 'time_taken', 'answer_array' , 'int_answer' , 'marks_obtained')

admin.site.register(Answer, AnswerAdmin)
