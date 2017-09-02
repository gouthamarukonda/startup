from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from paper.models import Mapping
from django.contrib.postgres.fields import ArrayField
from question.models import Question

class Answer(models.Model):

	answer_id = models.AutoField("Answer ID", db_column = 'answer_id', primary_key = True)
	user = models.ForeignKey(User, db_column = 'user_id', on_delete = models.CASCADE)
	mapping = models.ForeignKey(Mapping, db_column = 'map_id', on_delete = models.CASCADE)
	answer_array = ArrayField(models.CharField(max_length = 2), blank = True, null = True)
	int_answer = models.IntegerField("Integer Answer", blank = True, null = True)
	marks_obtained = models.FloatField("Marks Obtained", default = 0)
	time_taken = models.IntegerField("Time Taken", default = 0.0)
	time_stamp = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'answer'

	def __unicode__(self):
		return unicode(self.answer_id)
