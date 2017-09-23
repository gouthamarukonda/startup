from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from .approvalTypes import *

STATUS_WAITING = '0'
STATUS_APPROVED = '1'
STATUS_NOT_APPROVED = '2'

STATUS_CHOICES = (
	(STATUS_WAITING, "Waiting for Approval"),
	(STATUS_APPROVED, "Request Approved"),
	(STATUS_NOT_APPROVED, "Request Not Approved")
)

class ApprovalRequest(models.Model):

	approval_request_id = models.AutoField("Approval ID", db_column = 'approval_id', primary_key = True)
	approval_type = models.CharField("Paper Type", max_length = 2, choices = APPROVAL_TYPES, default = APPROVAL_NO_ACTION)
	user = models.ForeignKey(User, db_column = 'user_id', on_delete = models.CASCADE)
	status = models.CharField("Approval Status", choices = STATUS_CHOICES, max_length = 1, default = STATUS_WAITING)
	data = models.CharField("Data", max_length = 512, blank = True, null = True)
	comment = models.TextField("comment", blank = True, null = True)

	class Meta:
		db_table = 'approval_request'

	def __unicode__(self):
		return unicode(self.approval_request_id)
