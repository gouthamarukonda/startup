from django.contrib.postgres.fields import ArrayField
from django.db import models


class MultipleChoiceQuestion(models.Model):

    question = models.OneToOneField('question.Question', db_column = 'question_id', primary_key = True, on_delete = models.CASCADE)
    options = ArrayField(ArrayField(models.TextField(), size = 3), blank = True, null = True)

class MultipleChoiceAnswer(models.Model):

    answer = models.OneToOneField('question.Answer', db_column = 'answer_id', primary_key = True, on_delete = models.CASCADE)
    answer_array = ArrayField(models.CharField(max_length = 2), blank = True, null = True)
