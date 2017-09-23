from django.contrib import admin

from .models import TeacherProfile

class TeacherProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'experience')
	fields = ('user', 'experience')

admin.site.register(TeacherProfile, TeacherProfileAdmin)
