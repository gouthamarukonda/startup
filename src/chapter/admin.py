from django.contrib import admin

from .models import Chapter

class ChapterAdmin(admin.ModelAdmin):
	list_display = ( 'chapter_id', 'chapter_name', 'subject')
	fields = ( 'chapter_name', 'subject')

admin.site.register(Chapter, ChapterAdmin)
