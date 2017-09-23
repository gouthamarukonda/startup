from django.contrib import admin

from .models import SubjectiveAnswer


class SubjectiveAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'subjective_answer')
    fields = ('subjective_answer',)

admin.site.register(SubjectiveAnswer, SubjectiveAnswerAdmin)
