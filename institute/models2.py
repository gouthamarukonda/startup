from __future__ import unicode_literals

from django.db import models

from .models import Institute
from userprofile.models import UserProfile

class InstituteAdmin(models.Model):

	user = models.OneToOneField(UserProfile, db_column = 'user_id', primary_key = True, on_delete = models.CASCADE)
	institutes = models.ManyToManyField(Institute)

	class Meta:
		db_table = 'institute_admin'

	def __unicode__(self):
		return unicode(self.user)
