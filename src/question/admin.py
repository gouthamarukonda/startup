from django.contrib import admin

from .models import Question

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question_id', 'chapter_id', 'question_type', 'question', 'question_image', 'marks_positive' , 'marks_negative' , 'options' , 'int_answer' , 'solution' , 'solution_image' , 'complexity' , 'teacher_id' , 'time_stamp')
	fields = ('chapter_id', 'question_type', 'question', 'question_image', 'marks_positive' , 'marks_negative' , 'options' , 'int_answer' , 'solution' , 'solution_image' , 'complexity' , 'teacher_id')

admin.site.register(Question, QuestionAdmin)
