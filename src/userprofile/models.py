from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from institute.models import Institute

# Create your models here.

class UserProfile(models.Model):

	ROLE_STUDENT = '0'
	ROLE_TEACHER = '1'

	ROLE_CHOICES = (
		(ROLE_STUDENT, 'student'),
		(ROLE_TEACHER, 'teacher'),
	)

	user = models.OneToOneField(User, primary_key = True, db_column = 'user_id', on_delete = models.CASCADE)
	role = models.CharField("Role", choices = ROLE_CHOICES, db_column = 'role', default = ROLE_STUDENT, max_length = 1)
	mobile = models.IntegerField("Mobile Number", db_column = 'mobile', null = True, blank = True)
	institute = models.ForeignKey(Institute, blank = True, null = True, db_column = 'institute', on_delete = models.CASCADE)
	dob = models.DateTimeField("Date of Birth", db_column = 'dob', blank = True, null = True)
	
	class Meta:
		db_table = 'userprofile'

	def __unicode__(self):
		return unicode(self.user)