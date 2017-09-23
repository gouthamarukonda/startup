from django.contrib import admin

from .models import Question

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question_id', 'chapter', 'question_type', 'question', 'question_image', 'marks_positive' , 'marks_negative' , 'options' , 'int_answer' , 'solution' , 'solution_image' , 'complexity' , 'teacher' , 'time_stamp')
	fields = ('chapter', 'question_type', 'question', 'question_image', 'marks_positive' , 'marks_negative' , 'options' , 'int_answer' , 'solution' , 'solution_image' , 'complexity' , 'teacher')

admin.site.register(Question, QuestionAdmin)
