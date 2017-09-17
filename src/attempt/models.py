from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from paper.models import Paper

STATUS_NOT_STARTED = '0'
STATUS_ONGOING = '1'
STATUS_FINISHED = '2'

STATUS_CHOICES = (
	(STATUS_NOT_STARTED, "Not Started"),
	(STATUS_ONGOING, "Ongoing"),
	(STATUS_FINISHED, "Finished")
)

class Attempt(models.Model):

	attempt_id = models.AutoField("Attempt ID", db_column = 'attempt_id', primary_key = True)
	user = models.ForeignKey(User, db_column = 'user_id', on_delete = models.CASCADE)
	paper = models.ForeignKey(Paper, db_column = 'paper_id', on_delete = models.CASCADE)
	status = models.CharField("Attempt Status", choices = STATUS_CHOICES, max_length = 1, default = STATUS_NOT_STARTED)
	start_time = models.DateTimeField(auto_now = False, blank = True, null = True)
	end_time = models.DateTimeField(auto_now = False, blank = True, null = True)
