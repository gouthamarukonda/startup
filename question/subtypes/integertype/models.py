from django.db import models


class IntegerTypeQuestion(models.Model):

    question = models.OneToOneField('question.Question', db_column = 'question_id', primary_key = True, on_delete = models.CASCADE)
    int_answer = models.IntegerField("Integer Answer", blank = True, null = True)

class IntegerTypeAnswer(models.Model):

    answer = models.OneToOneField('question.Answer', db_column = 'answer_id', primary_key = True, on_delete = models.CASCADE)
    int_answer = models.IntegerField("Integer Answer", blank = True, null = True)
