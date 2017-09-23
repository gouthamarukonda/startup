
from integertype.tools import create_integer_type_question, update_integer_type_answer, evaluate_integer_type_answer
from multiplechoice.tools import create_multiple_choice_question, update_multiple_choice_answer, evaluate_multiple_choice_answer
from subjective.tools import update_subjective_answer
from .types import *


def create_sub_question(request, question):

    if question.question_type == Q_MULTIPLE_CHOICE:
        create_multiple_choice_question(request, question)

    elif question.question_type == Q_INTEGER:
        create_integer_type_question(request, question)

    elif question.question_type == Q_SUBJECTIVE:
        pass

    else:
        raise Exception("create_sub_question not defined for question_type=" + question.get_question_type_display())

def update_sub_answer_and_evaluate(request, answer):

    if answer.question.question_type == Q_MULTIPLE_CHOICE:
        update_multiple_choice_answer(request, answer)
        evaluate_multiple_choice_answer(answer)

    elif answer.question.question_type == Q_INTEGER:
        update_integer_type_answer(request, answer)
        evaluate_integer_type_answer(answer)

    elif answer.question.question_type == Q_SUBJECTIVE:
        update_subjective_answer(request, answer)

    else:
        raise Exception("update_sub_answer_and_evaluate not defined for question_type=" + answer.question.get_question_type_display())
