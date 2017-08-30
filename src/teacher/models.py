from __future__ import unicode_literals

from django.db import models
from userprofile.models import UserProfile

# Create your models here.

class TeacherProfile(models.Model):

	user = models.OneToOneField(UserProfile, primary_key = True, db_column = 'user_id', on_delete = models.CASCADE)
	experience = models.CharField("Experience", max_length = 5000, null = True, blank = True)

	class Meta:
		db_table = 'teacher_profile'

	def __unicode__(self):
		return unicode(self.user)