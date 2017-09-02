from __future__ import unicode_literals

from django.db import models
from chapter.models import Chapter
from teacher.models import TeacherProfile
from django.contrib.postgres.fields import ArrayField

Q_MULTIPLE = '0'
Q_SINGLE = '1'
Q_MATRIX = '2'
Q_INTEGER = '3'

QUESTION_CHOICES = (
	(Q_MULTIPLE, 'multiple'),
	(Q_SINGLE, 'single'),
	(Q_MATRIX, 'matrix'),
	(Q_INTEGER, 'integer')
)

C_VERYEASY = '0'
C_EASY = '1'
C_MEDIUM = '2'
C_HARD = '3'
C_VERYHARD = '4'

COMPLEXITY_CHOICES = (
	(C_VERYEASY, 'Very Easy'),
	(C_EASY, 'Easy'),
	(C_MEDIUM, 'Medium'),
	(C_HARD, 'Hard'),
	(C_VERYHARD, 'Very Hard')
)

class Question(models.Model):
	question_id = models.AutoField("Question ID", db_column = 'question_id', primary_key = True)
	chapter = models.ForeignKey(Chapter, db_column = 'chapter_id', on_delete = models.CASCADE)
	question_type = models.CharField("Question Type", max_length = 1, choices = QUESTION_CHOICES, default = Q_SINGLE)
	question = models.TextField("Question", blank = True, null = True)
	question_image = models.TextField("Question Image", blank = True, null = True)
	marks_positive = models.IntegerField("Positive Marks", default = 3)
	marks_negative = models.IntegerField("Negative Marks", default = -1)
	options = ArrayField(ArrayField(models.TextField(), size = 3), blank = True, null = True)
	int_answer = models.IntegerField("Integer Answer", blank = True, null = True)
	solution = models.TextField("Solution", db_column = 'solution', blank = True, null = True)
	solution_image = models.TextField("Solution Image", blank = True, null = True)
	complexity = models.CharField("Question Complexity", max_length = 1, choices = COMPLEXITY_CHOICES, default = C_EASY)
	teacher = models.ForeignKey(TeacherProfile, db_column = 'teacher_id', on_delete = models.CASCADE)
	time_stamp = models.DateTimeField(auto_now = True, blank = True, null = True)

	class Meta:
		db_table = 'question'

	def __unicode__(self):
		return unicode(self.question_id)
