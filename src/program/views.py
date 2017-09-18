import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from program.models import Program, Standard
from userprofile.decorators import admin_required

@csrf_exempt
@admin_required
def program_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("program_name"):
				return JsonResponse({"status": False, "msg": "Program Name shouldn't be empty"})
			
			program = Program()
			program.program_name = request.POST.get("program_name")

			try:
				program.save()
				program.subjects.add(*map(int, json.loads(request.POST.get("subject_list"))["subject_list"]))
				return JsonResponse({"status": True, "msg": "Program Registered Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
def get_all_programs(request):
	if request.method == 'GET':
		try:
			resp = {"status": True}
			resp["programs"] = []
			for program in Program.objects.all():
				odict={
					"program_id" : program.program_id,
					"program_name" : program.program_name,
				}
				resp["programs"].append(odict)
			return JsonResponse(resp)
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

@csrf_exempt
def get_all_standards(request):
	if request.method == 'GET':
		try:
			resp = {"status": True}
			resp["standards"] = []
			for standard in Standard.objects.all():
				odict={
					"standard_id" : standard.standard_id,
					"standard_name" : standard.standard_name,
				}
				resp["standards"].append(odict)
			return JsonResponse(resp)
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})