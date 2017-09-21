import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from program.models import Program, Standard
from chapter.models import Subject
from userprofile.decorators import admin_required

@csrf_exempt
@admin_required
def program_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("program_name"):
				return JsonResponse({"status": False, "msg": "Program Name shouldn't be empty"})

			subject_ids = json.loads(request.POST.get("subject_list"))["subject_list"]
			if not len(subject_ids)==len(Subject.objects.filter(pk__in = subject_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Subject IDs are invalid or appear more than once"})
			
			program = Program()
			program.program_name = request.POST.get("program_name")

			try:
				program.save()
				program.subjects.add(*map(int, subject_ids))
				return JsonResponse({"status": True, "msg": "Program Registered Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def standard_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("standard_name"):
				return JsonResponse({"status": False, "msg": "Standard Name shouldn't be empty"})

			if Standard.objects.filter(standard_name = request.POST.get("standard_name")).exists():
				return JsonResponse({"status": False, "msg": "Standard already exists"})
			
			standard = Standard()
			standard.standard_name = request.POST.get("standard_name")

			try:
				standard.save()
				return JsonResponse({"status": True, "msg": "Standard added Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})