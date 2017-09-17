import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import datetime

from userprofile.decorators import student_required
from question.models import Question, Q_INTEGER
from attempt.models import Attempt
from .models import Answer
from .tools import evaluate_answer

@csrf_exempt
@student_required
def submit_answer(request):
	if request.method == 'POST':

		try:
			if not Question.objects.filter(question_id = request.POST.get("question_id")).exists():
				return JsonResponse({"status": False, "msg": "Question doesn't exist"})

			if not Attempt.objects.filter(attempt_id = request.POST.get("attempt_id")).exists():
				return JsonResponse({"status": False, "msg": "Attempt doesn't exist"})

			question = Question.objects.get(question_id = request.POST.get("question_id"))
			attempt = Attempt.objects.get(attempt_id = request.POST.get("attempt_id"))
			answer = None
			if Answer.objects.filter(question = question, attempt = attempt).exists():
				answer = Answer.objects.get(user = request.user, question = question, attempt = attempt)
			else:
				answer = Answer(question = question, attempt = attempt)

			if question.question_type == Q_INTEGER:
				answer.int_answer = int(request.POST.get("int_answer"))
			else:
				answer.answer_array = json.loads(request.POST.get("answer_array"))["answer_array"]

			if request.POST.get("time_taken"):
				answer.time_taken += int(request.POST.get("time_taken"))

			answer.status = request.POST.get("status")
			answer.marks_obtained = evaluate_answer(attempt.paper, question, answer)
			answer.save()
			return JsonResponse({"status": True, "msg": "Answer Saved"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
