import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required

from question.models import Question
from paper.models import Paper, PM_CHOICES, PaperType
from userprofile.decorators import admin_required, teacher_required
from program.models import Program
from institute.models import Institute

@csrf_exempt
@teacher_required
def paper_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("paper_name"):
				return JsonResponse({"status": False, "msg": "Paper Name shouldn't be empty"})

			if not PaperType.objects.filter(type_id = request.POST.get("paper_type")).exists():
				return JsonResponse({"status": False, "msg": "Paper Type does not exist"})

			if not Program.objects.filter(program_id = request.POST.get("program_id")).exists():
				return JsonResponse({"status": False, "msg": "Program ID does not exist"})

			if request.POST.get("partial_marking") not in [choice[0] for choice in PM_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Partial Marking Scheme"})

			institute_ids = json.loads(request.POST.get("institute_list"))["institute_list"]
			standard_ids = json.loads(request.POST.get("standard_list"))["standard_list"]

			if not len(institute_ids)==len(Institute.objects.filter(pk__in = institute_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Institute IDs are invalid or appear more than once"})
			
			if not len(standard_ids)==len(Institute.objects.filter(pk__in = standard_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Standard IDs are invalid or appear more than once"})
				
			paper = Paper()
			paper.paper_name = request.POST.get("paper_name")
			paper.program = Program.objects.get(program_id = request.POST.get("program_id"))
			paper.paper_type = PaperType.objects.get(type_id = request.POST.get("paper_type"))
			paper.teacher_id = request.user.userprofile.teacherprofile
			paper.start_time = datetime.now()
			paper.end_time = datetime.now()
			paper.duration = request.POST.get("duration")
			paper.partial_marking = request.POST.get("partial_marking")

			try:
				paper.save()
				pk_id = json.loads(request.POST.get("institute_list"))["institute_list"]
				paper.institutes.add(*map(int, institute_ids))
				paper.standards.add(*map(int, standard_ids))
				return JsonResponse({"status": True, "msg": "Paper Registered Successfully"})
			except:
				paper.delete()
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})


@csrf_exempt
@teacher_required
def add_question(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("paper_id"):
				return JsonResponse({"status": False, "msg": "Paper ID shouldn't be empty"})

			if not Paper.objects.filter(paper_id = request.POST.get("paper_id")).exists():
				return JsonResponse({"status": False, "msg": "Paper ID does not exist"})
			
			paper = Paper.objects.get(paper_id = request.POST.get("paper_id"))
			paper.questions.add(request.POST.get("question_id"))

			return JsonResponse({"status": True, "msg": "Question added Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})


@csrf_exempt
@admin_required
def paper_type_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("paper_type"):
				return JsonResponse({"status": False, "msg": "Paper Type shouldn't be empty"})

			if PaperType.objects.filter(type_name = request.POST.get("paper_type")).exists():
				return JsonResponse({"status": False, "msg": "Paper Type already exists"})
			
			paper_type = PaperType()
			paper_type.type_name = request.POST.get("paper_type")
			
			try:
				paper_type.save()
				return JsonResponse({"status": True, "msg": "Paper Type Added Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})