from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from paper.models import Paper
from django.contrib.postgres.fields import ArrayField
from question.models import Question

# Create your models here.


class Answer(models.Model):

	answer_id = models.AutoField("Answer ID", db_column = 'answer_id', primary_key = True)
	user_id = models.ForeignKey(User, db_column = 'user_id', on_delete = models.CASCADE)
	dpp_id = models.ForeignKey(Paper, db_column = 'dpp_id', on_delete = models.CASCADE)
	question_id = models.ForeignKey(Question, db_column = 'question_id', on_delete = models.CASCADE)
	time_taken = models.DateTimeField(auto_now = False, blank = True, null = True)
	answer_array = ArrayField(models.TextField(blank = True, null = True, default = None) ,size=3)
	int_answer = models.IntegerField("Integer Answer", blank = True, null = True, default = None)
	marks_obtained = models.IntegerField("Marks Obtained", default = 0)
	time_stamp = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'answer'

	def __unicode__(self):
		return unicode(self.paper_name)