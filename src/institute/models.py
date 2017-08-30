from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Institute(models.Model):

	institute_id = models.AutoField("Institute ID", primary_key = True, db_column = 'institute_id')
	institute_name = models.CharField("Institute Name", max_length = 500, null = True, blank = True)
	address = models.CharField("Institute Address", max_length = 5000, null = True, blank = True)
	city = models.CharField("Institute City", max_length = 500, null = True, blank = True)
	state = models.CharField("Institute State", max_length = 500, null = True, blank = True)
	phone_no = models.IntegerField("Institute Phone_No", null = True, blank = True)
	manager_name = models.CharField("Institute Manager name", max_length = 500, null = True, blank = True)



	class Meta:
		db_table = 'institute'

	def __unicode__(self):
		return unicode(self.institute_name)
