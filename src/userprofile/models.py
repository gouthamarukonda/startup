from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from institute.models import Institute

ROLE_STUDENT = '0'
ROLE_TEACHER = '1'

ROLE_CHOICES = (
	(ROLE_STUDENT, 'student'),
	(ROLE_TEACHER, 'teacher'),
)

STATUS_UNAPPROVED = '0'
STATUS_APPROVED = '1'

STATUS_CHOICES = (
	(STATUS_APPROVED, "Registration Approved"),
	(STATUS_UNAPPROVED, "Registration Not Approved"),
)

class UserProfile(models.Model):

	user = models.OneToOneField(User, db_column = 'user_id', primary_key = True, on_delete = models.CASCADE)
	role = models.CharField("Role", db_column = 'role', choices = ROLE_CHOICES, max_length = 1, default = ROLE_STUDENT)
	mobile = models.CharField("Mobile Number", db_column = 'mobile', max_length = 15, blank = True)
	institute = models.ForeignKey(Institute, db_column = 'institute', on_delete = models.CASCADE)
	dob = models.DateTimeField("Date of Birth", db_column = 'dob', blank = True)
	status = models.CharField("Registration Status", db_column = 'status', choices = STATUS_CHOICES, max_length = 1, default = STATUS_UNAPPROVED)

	class Meta:
		db_table = 'user_profile'

	def __unicode__(self):
		return unicode(self.user)
