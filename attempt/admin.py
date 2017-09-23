from django.contrib import admin

from .models import Attempt

class AttemptAdmin(admin.ModelAdmin):
	list_display = ('attempt_id', 'user', 'paper', 'status', 'start_time', 'end_time')
	fields = ('user', 'paper', 'status', 'start_time', 'end_time')

admin.site.register(Attempt, AttemptAdmin)
