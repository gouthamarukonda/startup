from django.db import models


class SubjectiveAnswer(models.Model):

    answer = models.OneToOneField('question.Answer', db_column = 'answer_id', primary_key = True, on_delete = models.CASCADE)
    subjective_answer = models.TextField("Subjective Answer", db_column = 'subjective_answer', blank = True, null = True)
    is_evaluated = models.BooleanField("Is Evaluated ?", default = False)
