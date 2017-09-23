import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from attempt.models import Attempt
from chapter.models import Chapter
from question.models import Question, COMPLEXITY_CHOICES, QUESTION_CHOICES, Q_INTEGER, Answer
from subtypes.router import create_sub_question, update_sub_answer_and_evaluate
from userprofile.decorators import teacher_required, student_required


@csrf_exempt
@teacher_required
def question_create(request):
	if request.method == 'POST':

		try:
			if request.POST.get("question_type") not in [choice[0] for choice in QUESTION_CHOICES]:
				return JsonResponse({"status": False, "msg": "Invalid Question Type"})

			chapter_ids = json.loads(request.POST.get("chapters"))["chapters"]
			if not len(chapter_ids) == len(Chapter.objects.filter(pk__in = chapter_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Chapter IDs are invalid or appear more than once"})

			if not request.POST.get("question"):
				return JsonResponse({"status": False, "msg": "question shouldn't be empty"})

			if request.POST.get("complexity") not in [choice[0] for choice in COMPLEXITY_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid complexity"})
			
			if request.POST.get("question_type") == Q_INTEGER and not request.POST.get("int_answer"):
				return JsonResponse({"status": False, "msg": "Integer answer can't be empty"})

			question = Question()
			question.question_type = request.POST.get("question_type")
			question.teacher = request.user.userprofile.teacherprofile
			question.question = request.POST.get("question")
			question.solution = request.POST.get("solution")
			question.complexity = request.POST.get("complexity")
			question.marks_positive = request.POST.get("marks_positive")
			question.marks_negative = request.POST.get("marks_negative")

			if 'question_image' in request.FILES:
				question.question_image = request.FILES["question_image"]
			if 'solution_image' in request.FILES:
				question.solution_image = request.FILES["solution_image"]

			question.save()
			question.chapters.add(*map(int, chapter_ids))

			try:
				create_sub_question(request, question)
			except Exception as e:
				question.delete()
				return JsonResponse({"status": True, "msg": str(e)})

			return JsonResponse({"status": True, "msg": "Question Registered Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})


@csrf_exempt
@teacher_required
def question_delete(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("question_id"):
				return JsonResponse({"status": False, "msg": "question_id shouldn't be empty"})

			if not Question.objects.filter(question_id = request.POST.get("question_id")).exists():
				return JsonResponse({"status": False, "msg": "question doesn't exist"})

			question = Question.objects.get(question_id = request.POST.get("question_id"))
			question.delete()
			return JsonResponse({"status": True, "msg": "Question deleted successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

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

			if Answer.objects.filter(question = question, attempt = attempt).exists():
				answer = Answer.objects.get(question = question, attempt = attempt)
			else:
				answer = Answer(question = question, attempt = attempt)

			if request.POST.get("status"):
				answer.status = request.POST.get("status")

			if request.POST.get("time_taken"):
				answer.time_taken += int(request.POST.get("time_taken"))

			answer.save()

			try:
				update_sub_answer_and_evaluate(request, answer)
			except Exception as e:
				answer.delete()
				return JsonResponse({"status": False, "msg": str(e)})

			return JsonResponse({"status": True, "msg": "Answer Saved"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
