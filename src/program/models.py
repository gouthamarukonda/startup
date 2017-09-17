from __future__ import unicode_literals

from django.db import models

class Program(models.Model):
	program_id = models.AutoField("Program ID", db_column = 'program_id', primary_key = True)
	program_name = models.CharField("Program Name", max_length = 100, blank = True)

	class Meta:
		db_table = 'program'

	def __unicode__(self):
		return unicode(self.program_name)
