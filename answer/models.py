from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField

from question.models import Question
from attempt.models import Attempt

STATUS_UNSEEN = '0'
STATUS_UNANSWERED = '1'
STATUS_ANSWERED = '2'

ANSWER_STATUS = (
	(STATUS_UNSEEN, "Unseen"),
	(STATUS_UNANSWERED, "Seen and not Answered"),
	(STATUS_ANSWERED, "Answered")
)

class Answer(models.Model):

	answer_id = models.AutoField("Answer ID", db_column = 'answer_id', primary_key = True)
	question = models.ForeignKey(Question, db_column = 'question_id', on_delete = models.CASCADE)
	attempt = models.ForeignKey(Attempt, db_column = 'attempt_id', on_delete = models.CASCADE)
	answer_array = ArrayField(models.CharField(max_length = 2), blank = True, null = True)
	status = models.CharField("Status", max_length = 1, choices = ANSWER_STATUS, default = STATUS_UNSEEN)
	int_answer = models.IntegerField("Integer Answer", blank = True, null = True)
	marks_obtained = models.FloatField("Marks Obtained", default = 0)
	time_taken = models.IntegerField("Time Taken", default = 0.0)
	time_stamp = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'answer'

	def __unicode__(self):
		return unicode(self.answer_id)
