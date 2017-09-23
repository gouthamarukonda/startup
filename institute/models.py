from __future__ import unicode_literals

from django.db import models
from program.models import Program

class Institute(models.Model):

	institute_id = models.AutoField("Institute ID", db_column = 'institute_id', primary_key = True)
	institute_name = models.CharField("Institute Name", max_length = 500)
	programs = models.ManyToManyField(Program)
	address = models.CharField("Institute Address", max_length = 5000, blank = True)
	city = models.CharField("Institute City", max_length = 500, blank = True)
	state = models.CharField("Institute State", max_length = 500, blank = True)
	phone_no = models.CharField("Institute Phone_No", max_length = 15, null = True, blank = True)
	manager_name = models.CharField("Institute Manager name", null = True, max_length = 500, blank = True)

	class Meta:
		db_table = 'institute'

	def __unicode__(self):
		return unicode(self.institute_name)

	def PROGRAMS(self):
		return ", ".join([str(p.program_name) for p in self.programs.all()])
