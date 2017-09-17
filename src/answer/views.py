import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import datetime

from userprofile.decorators import student_required
from question.models import Question, Q_INTEGER
from paper.models import Mapping
from .models import Answer
from .tools import evaluate_answer

@csrf_exempt
@student_required
def submit_answer(request):
	if request.method == 'POST':

		try:
			if not Mapping.objects.filter(map_id = request.POST.get("map_id")).exists():
				return JsonResponse({"status": False, "msg": "Paper-Question Mapping doesn't exist"})

			mapping = Mapping.objects.get(map_id = request.POST.get("map_id"))
			answer = None
			if Answer.objects.filter(user = request.user, mapping = mapping).exists():
				answer = Answer.objects.get(user = request.user, mapping = mapping)
			else:
				answer = Answer(user = request.user, mapping = mapping)

			if mapping.question.question_type == Q_INTEGER:
				answer.int_answer = int(request.POST.get("int_answer"))
			else:
				answer.answer_array = json.loads(request.POST.get("answer_array"))["answer_array"]

			if request.POST.get("time_taken"):
				answer.time_taken += int(request.POST.get("time_taken"))

			answer.status = request.POST.get("status")
			answer.marks_obtained = evaluate_answer(mapping.paper, mapping.question, answer)
			answer.save()
			return JsonResponse({"status": True, "msg": "Answer Saved"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
