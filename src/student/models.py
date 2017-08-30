from __future__ import unicode_literals

from django.db import models
from userprofile.models import UserProfile

# Create your models here.

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

	user = models.OneToOneField(UserProfile, primary_key = True, db_column = 'user_id', on_delete = models.CASCADE)
	standard = models.CharField("Standard", max_length = 11, null = True, blank = True)
	boe = models.CharField("Board of Education", max_length = 500, null = True, blank = True)

	class Meta:
		db_table = 'student_profile'

	def __unicode__(self):
		return unicode(self.user)