from django.contrib import admin

# Register your models here.

from .models import ApprovalRequest

class ApprovalRequestAdmin(admin.ModelAdmin):
	list_display = ('approval_request_id', 'approval_type', 'user', 'status', 'data')
	fields = ('approval_type', 'user', 'status', 'data')

admin.site.register(ApprovalRequest, ApprovalRequestAdmin)
