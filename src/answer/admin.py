from django.contrib import admin

from .models import Answer

class AnswerAdmin(admin.ModelAdmin):
	list_display = ( 'answer_id', 'user_id', 'dpp_id', 'question_id', 'time_taken', 'answer_array' , 'int_answer' , 'marks_obtained' , 'time_stamp')
	fields = ( 'user_id', 'dpp_id', 'question_id', 'time_taken', 'answer_array' , 'int_answer' , 'marks_obtained')

admin.site.register(Answer, AnswerAdmin)
