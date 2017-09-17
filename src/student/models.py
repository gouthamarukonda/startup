from __future__ import unicode_literals

from django.db import models
from userprofile.models import UserProfile

STD_8 = '0'
STD_9 = '1'
STD_10 = '2'
STD_11 = '3'
STD_12 = '4'

STD_CHOICES = (
	(STD_8, '8'),
	(STD_9, '9'),
	(STD_10, '10'),
	(STD_11, '11'),
	(STD_12, '12'),
)

class StudentProfile(models.Model):

	user = models.OneToOneField(UserProfile, db_column = 'user_id', primary_key = True, on_delete = models.CASCADE)
	standard = models.CharField("Standard", max_length = 2, choices = STD_CHOICES, blank = True)
	boe = models.CharField("Board of Education", max_length = 500, blank = True)
	roll_number = models.CharField("Roll Number", max_length = 32, blank = True, null = True)

	class Meta:
		db_table = 'student_profile'

	def __unicode__(self):
		return unicode(self.user)
