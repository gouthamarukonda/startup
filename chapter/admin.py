from django.contrib import admin

from .models import Chapter, Subject

class ChapterAdmin(admin.ModelAdmin):
	list_display = ('chapter_id', 'chapter_name', 'subject')
	fields = ('chapter_name', 'subject')

class SubjectAdmin(admin.ModelAdmin):
	list_display = ('subject_id', 'subject_name')
	fields = ('subject_name', )

admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Subject, SubjectAdmin)
