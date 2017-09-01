from __future__ import unicode_literals

from django.db import models
from teacher.models import TeacherProfile
from question.models import Question


PM_NO = '0'
PM_YES = '1'


PM_CHOICES = (
	(PM_YES, 'Yes'),
	(PM_NO, 'No')
)

PAPER_DPP = '0'
PAPER_EXAM = '1'


PAPER_CHOICES = (
	(PAPER_DPP, 'Dpp'),
	(PAPER_EXAM, 'Exam')
)

class Paper(models.Model):

	paper_id = models.AutoField("Paper ID", db_column = 'paper_id', primary_key = True)
	paper_name = models.CharField("Paper Name", max_length = 600, blank = True)
	paper_type = models.CharField("Paper Type", max_length = 1, choices = PAPER_CHOICES, default = PAPER_DPP)
	teacher_id = models.ForeignKey(TeacherProfile, db_column = 'teacher_id', on_delete = models.CASCADE)
	start_time = models.DateTimeField(auto_now = False, blank = True, null = True)
	end_time = models.DateTimeField(auto_now = False, blank = True, null = True)
	partial_marking = models.CharField("Partial Marking", max_length = 1, choices = PM_CHOICES, default = PM_NO)
	time_stamp = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'paper'

	def __unicode__(self):
		return unicode(self.paper_name)



class Mapping(models.Model):

	map_id = models.AutoField("Paper ID", db_column = 'map_id', primary_key = True)
	question_id = models.ForeignKey(Question, db_column = 'question_id', on_delete = models.CASCADE)
	paper_id = models.ForeignKey(Paper, db_column = 'paper_id', on_delete = models.CASCADE)

	class Meta:
		db_table = 'mapping'

	def __unicode__(self):
		return unicode(self.map_id)

