import json

from paper.models import PM_YES
from .models import MultipleChoiceQuestion, MultipleChoiceAnswer


def create_multiple_choice_question(request, question):

    if not request.POST.get("options"):
        raise Exception("options cannot be empty")

    try:
        multiple_choice_question = MultipleChoiceQuestion()
        multiple_choice_question.question = question
        multiple_choice_question.options = json.loads(request.POST.get("options"))["options"]
        multiple_choice_question.save()
    except:
        raise Exception("Internal Server Error")

def update_multiple_choice_answer(request, answer):

    if not request.POST.get("answer_array"):
        raise Exception("answer_array cannot be empty")

    try:
        if not hasattr(answer, 'multiplechoiceanswer'):
            multiple_choice_answer = MultipleChoiceAnswer()
            multiple_choice_answer.answer = answer
        else:
            multiple_choice_answer = answer.multiplechoiceanswer

        multiple_choice_answer.answer_array = json.loads(request.POST.get("answer_array"))["answer_array"]
        multiple_choice_answer.save()

    except:
        raise Exception("Internal Server Error")

def evaluate_multiple_choice_answer(answer):

    try:
        submitted_answer = answer.multiplechoiceanswer.answer_array
        actual_answer = [option[0] for option in answer.question.multiplechoicequestion.options if option[1] == '1']
        num_correct = 0
        num_wrong = 0

        for option in submitted_answer:
            if option in actual_answer:
                num_correct += 1
            else:
                num_wrong += 1

        if num_wrong > 0:
            answer.marks_obtained = answer.question.marks_negative

        elif answer.attempt.paper.partial_marking == PM_YES:
            answer.marks_obtained = answer.question.marks_positive * num_correct * 1.0 / len(actual_answer)

        elif num_correct == len(actual_answer):
            answer.marks_obtained = answer.question.marks_positive

        else:
            answer.marks_obtained = answer.question.marks_negative
        answer.save()

    except:
        raise Exception("Internal Server Error")
