from __future__ import unicode_literals

from django.db import models

# Create your models here.


SUBJECT_MATHS = '0'
SUBJECT_PYHSICS = '1'
SUBJECT_CHEMISTRY = '2'	

SUBJECT_CHOICES = (
	(SUBJECT_MATHS, 'maths'),
	(SUBJECT_PYHSICS, 'physics'),
	(SUBJECT_CHEMISTRY, 'chemistry'),
)	

class Chapter(models.Model):

	chapter_id = models.AutoField("Chapter ID", primary_key = True, db_column = 'chapter_id')
	chapter_name = models.CharField("Chapter Name", max_length = 500, null = True, blank = True)
	subject = models.CharField("Subject", choices = SUBJECT_CHOICES, max_length = 1)



	class Meta:
		db_table = 'chapter'

	def __unicode__(self):
		return unicode(self.chapter_name)
