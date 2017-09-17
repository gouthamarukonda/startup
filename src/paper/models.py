from __future__ import unicode_literals

from django.db import models
from teacher.models import TeacherProfile
from question.models import Question
from program.models import Program
from institute.models import Institute

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
	program = models.ForeignKey(Program, db_column = 'program_id', on_delete = models.PROTECT)
	institutes = models.ManyToManyField(Institute, db_column = 'institute_ids')
	questions = models.ManyToManyField(Question, db_column = 'question_ids')
	paper_name = models.CharField("Paper Name", max_length = 600, blank = True)
	paper_type = models.CharField("Paper Type", max_length = 1, choices = PAPER_CHOICES, default = PAPER_DPP)
	teacher_id = models.ForeignKey(TeacherProfile, db_column = 'teacher_id', on_delete = models.CASCADE)
	start_time = models.DateTimeField(auto_now = False, blank = True, null = True)
	end_time = models.DateTimeField(auto_now = False, blank = True, null = True)
	duration = models.IntegerField("Duration", blank = True, default = 180)
	partial_marking = models.CharField("Partial Marking", max_length = 1, choices = PM_CHOICES, default = PM_NO)
	time_stamp = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'paper'

	def __unicode__(self):
		return unicode(self.paper_id)

	def INSTITUTES(self):
		return ", ".join([str(p.institute_id) for p in self.institutes.all()])

	def QUESTIONS(self):
		return ", ".join([str(p.question_id) for p in self.questions.all()])
