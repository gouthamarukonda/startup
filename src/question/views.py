import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required

from userprofile.decorators import teacher_required
from question.models import Question, COMPLEXITY_CHOICES, QUESTION_CHOICES, Q_INTEGER
from chapter.models import Chapter
from teacher.models import TeacherProfile
from paper.models import Paper, Mapping

@csrf_exempt
@teacher_required
def question_create(request):
	if request.method == 'POST':

		try:
			if not Paper.objects.filter(paper_id = request.POST.get("paper_id")).exists():
				return JsonResponse({"status": False, "msg": "Paper ID doesn't exist"})

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
			question.question_image = request.POST.get("question_image")
			question.marks_positive = request.POST.get("marks_positive")
			question.marks_negative = request.POST.get("marks_negative")
			question.solution = request.POST.get("solution")
			question.solution_image = request.POST.get("solution_image")
			question.complexity = request.POST.get("complexity")
			question.teacher = request.user.userprofile.teacherprofile
			if question.question_type == Q_INTEGER:
				question.int_answer = request.POST.get("int_answer")
			else:
				question.options = json.loads(request.POST.get("options"))["options"]
			question.save()

			mapping = Mapping()
			mapping.paper = Paper.objects.get(paper_id = request.POST.get("paper_id"))
			mapping.question = question

			try:
				mapping.save()
				return JsonResponse({"status": True, "msg": "Question Registered Successfully and Added to Paper"})
			except:
				return JsonResponse({"status": False, "msg": "Question Registered but unable to add to paper"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
