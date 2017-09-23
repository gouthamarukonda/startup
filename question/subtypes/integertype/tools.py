from .models import IntegerTypeQuestion, IntegerTypeAnswer


def create_integer_type_question(request, question):

    if not request.POST.get("int_answer"):
        raise Exception("int_answer cannot be empty")

    try:
        integer_type_question = IntegerTypeQuestion()
        integer_type_question.question = question
        integer_type_question.int_answer = int(request.POST.get("int_answer"))
        integer_type_question.save()
    except:
        raise Exception("Internal Server Error")

def update_integer_type_answer(request, answer):

    if not request.POST.get("int_answer"):
        raise Exception("int_answer cannot be empty")

    try:
        if not hasattr(answer, 'integertypeanswer'):
            integer_type_answer = IntegerTypeAnswer()
            integer_type_answer.answer = answer
        else:
            integer_type_answer = answer.integertypeanswer

        integer_type_answer.int_answer = int(request.POST.get("int_answer"))
        integer_type_answer.save()

    except:
        raise Exception("Internal Server Error")

def evaluate_integer_type_answer(answer):

    try:
        if answer.integertypeanswer.int_answer == answer.question.integertypequestion.int_answer:
            answer.marks_obtained = answer.question.marks_positive
        else:
            answer.marks_obtained = answer.question.marks_negative
        answer.save()

    except:
        raise Exception("Internal Server Error")
