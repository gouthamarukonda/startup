from django.contrib import admin

from .models import MultipleChoiceQuestion, MultipleChoiceAnswer


class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'options')
    fields = ('options',)

class MultipleChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'answer_array')
    fields = ('answer_array',)

admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(MultipleChoiceAnswer, MultipleChoiceAnswerAdmin)
