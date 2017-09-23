from django.contrib import admin

from .models import IntegerTypeQuestion, IntegerTypeAnswer


class IntegerTypeQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'int_answer')
    fields = ('int_answer',)

class IntegerTypeAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'int_answer')
    fields = ('int_answer',)

admin.site.register(IntegerTypeQuestion, IntegerTypeQuestionAdmin)
admin.site.register(IntegerTypeAnswer, IntegerTypeAnswerAdmin)
