from __future__ import unicode_literals

from django.db import models
from userprofile.models import UserProfile
from program.models import Standard

class StudentProfile(models.Model):

	user = models.OneToOneField(UserProfile, db_column = 'user_id', primary_key = True, on_delete = models.CASCADE)
	standard = models.ForeignKey(Standard, db_column = 'standard_id', on_delete = models.CASCADE)
	boe = models.CharField("Board of Education", max_length = 500, blank = True)
	roll_number = models.CharField("Roll Number", max_length = 32, blank = True, null = True)

	class Meta:
		db_table = 'student_profile'

	def __unicode__(self):
		return unicode(self.user)
