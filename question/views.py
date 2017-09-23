import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from chapter.models import Chapter
from question.models import Question, COMPLEXITY_CHOICES, QUESTION_CHOICES, Q_INTEGER
from userprofile.decorators import teacher_required


@csrf_exempt
@teacher_required
def question_create(request):
	if request.method == 'POST':

		try:
			if not Chapter.objects.filter(chapter_id = request.POST.get("chapter_id")).exists():
				return JsonResponse({"status": False, "msg": "Chapter ID doesn't exist"})

			if not request.POST.get("question"):
				return JsonResponse({"status": False, "msg": "question shouldn't be empty"})

			if request.POST.get("question_type") not in [choice[0] for choice in QUESTION_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Question Type"})

			if request.POST.get("complexity") not in [choice[0] for choice in COMPLEXITY_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid complexity"})
			
			if request.POST.get("question_type") == Q_INTEGER and not request.POST.get("int_answer"):
				return JsonResponse({"status": False, "msg": "Integer answer can't be empty"})

			question = Question()
			question.chapter = Chapter.objects.get(chapter_id = request.POST.get("chapter_id"))
			question.question_type = request.POST.get("question_type")
			question.question = request.POST.get("question")
			question.marks_positive = request.POST.get("marks_positive")
			question.marks_negative = request.POST.get("marks_negative")
			question.solution = request.POST.get("solution")
			question.complexity = request.POST.get("complexity")
			question.teacher = request.user.userprofile.teacherprofile

			if 'question_image' in request.FILES:
				question.question_image = request.FILES["question_image"]
			if 'solution_image' in request.FILES:
				question.solution_image = request.FILES["solution_image"]

			if question.question_type == Q_INTEGER:
				question.int_answer = request.POST.get("int_answer")
			else:
				question.options = json.loads(request.POST.get("options"))["options"]

			question.save()
			return JsonResponse({"status": True, "msg": "Question Registered Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
