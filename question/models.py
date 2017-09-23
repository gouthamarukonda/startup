from __future__ import unicode_literals

from django.db import models
from imagekit.models import ProcessedImageField

from attempt.models import Attempt
from chapter.models import Chapter
from subtypes.types import *
from teacher.models import TeacherProfile

''' While creating migrations, model classes need to be accessible from APP_DIR.models '''

from subtypes.multiplechoice.models import MultipleChoiceQuestion, MultipleChoiceAnswer
from subtypes.integertype.models import IntegerTypeQuestion, IntegerTypeAnswer
from subtypes.subjective.models import SubjectiveAnswer


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
	(C_VERYHARD, 'Very Hard'),
)

STATUS_UNSEEN = '0'
STATUS_UNANSWERED = '1'
STATUS_ANSWERED = '2'

ANSWER_STATUS = (
	(STATUS_UNSEEN, "Unseen"),
	(STATUS_UNANSWERED, "Seen and not Answered"),
	(STATUS_ANSWERED, "Answered"),
)

class Question(models.Model):

	question_id = models.AutoField("Question ID", db_column = 'question_id', primary_key = True)
	question_type = models.CharField("Question Type", max_length = 1, choices = QUESTION_CHOICES, default = Q_MULTIPLE_CHOICE)
	teacher = models.ForeignKey(TeacherProfile, db_column = 'teacher_id', on_delete=models.CASCADE)
	chapters = models.ManyToManyField(Chapter)
	question = models.TextField("Question", db_column = 'question', blank = True, null = True)
	solution = models.TextField("Solution", db_column = 'solution', blank = True, null = True)
	question_image = ProcessedImageField(upload_to = 'questions',
										 format = 'JPEG',
										 options = {'quality': 90},
										 null = True)
	solution_image = ProcessedImageField(upload_to = 'solutions',
										 format = 'JPEG',
										 options = {'quality': 90},
										 null = True)
	complexity = models.CharField("Question Complexity", max_length = 1, choices = COMPLEXITY_CHOICES, default = C_EASY)
	marks_positive = models.IntegerField("Positive Marks", default = 3)
	marks_negative = models.IntegerField("Negative Marks", default = -1)
	time_stamp = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'question'

	def __unicode__(self):
		return unicode(self.question_id)

	def CHAPTERS(self):
		return ", ".join([str(c.chapter_name) for c in self.chapters.all()])

class Answer(models.Model):

	answer_id = models.AutoField("Answer ID", db_column = 'answer_id', primary_key = True)
	question = models.ForeignKey(Question, db_column = 'question_id', on_delete = models.CASCADE)
	attempt = models.ForeignKey(Attempt, db_column = 'attempt_id', on_delete = models.CASCADE)
	status = models.CharField("Status", max_length = 1, choices = ANSWER_STATUS, default = STATUS_UNSEEN)
	marks_obtained = models.FloatField("Marks Obtained", default = 0)
	time_taken = models.IntegerField("Time Taken", default = 0)
	time_stamp = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'answer'

	def __unicode__(self):
		return unicode(self.answer_id)
