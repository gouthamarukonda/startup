from django.contrib import admin

from .models import Answer, Question


class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question_id', 'question_type', 'teacher', 'CHAPTERS', 'question', 'solution', 'question_image', 'solution_image' , 'complexity', 'marks_positive', 'marks_negative', 'time_stamp')
	fields = ('question_type', 'teacher', 'chapters', 'question', 'solution', 'question_image', 'solution_image' , 'complexity', 'marks_positive', 'marks_negative')

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('answer_id', 'question', 'attempt', 'status', 'marks_obtained', 'time_taken', 'time_stamp')
	fields = ('question', 'attempt', 'status', 'marks_obtained', 'time_taken')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

from subtypes.multiplechoice.admin import *
from subtypes.integertype.admin import *
from subtypes.subjective.admin import *
