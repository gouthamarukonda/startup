from .models import SubjectiveAnswer


def update_subjective_answer(request, answer):

    if not request.POST.get("subjective_answer"):
        raise Exception("subjective_answer cannot be empty")

    try:
        if not hasattr(answer, 'subjectiveanswer'):
            subjective_answer = SubjectiveAnswer()
            subjective_answer.answer = answer
        else:
            subjective_answer = answer.subjectiveanswer

        subjective_answer.subjective_answer = request.POST.get("subjective_answer")
        subjective_answer.save()

    except:
        raise Exception("Internal Server Error")
